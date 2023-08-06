from nbodykit.base.catalog import column
from nbodykit.source.catalog.array import ArrayCatalog
from nbodykit import CurrentMPIComm
from nbodykit.utils import GatherArray, ScatterArray

from six import add_metaclass
import abc
import logging
import numpy

def gal_type_integers(galtab):
    """
    Convert ``centrals`` to 0 and ``satellites`` to 1
    in the input galaxy Table

    This operatio is done in place
    """
    gal_type = numpy.zeros(len(galtab), dtype='i4')
    sats = galtab['gal_type'] == 'satellites'
    gal_type[sats] = 1
    galtab.replace_column('gal_type', gal_type)

def find_object_dtypes(data):
    """
    Utility function to convert 'O' data types to strings
    """
    for col in data.colnames:
        if data.dtype[col] == 'O':
            raise TypeError("column '%s' is of type 'O'; must convert to integer or string" %col)
    return data

class HODBase(ArrayCatalog):
    """
    A base class to be used for HOD population of a halo catalog.

    The user must supply the :func:`__makemodel__` function, which returns
    the halotools composite HOD model.

    This abstraction allows the user to potentially implement several
    different types of HOD models quickly, while using the population
    framework of this base class.
    """
    logger = logging.getLogger("HODBase")

    @CurrentMPIComm.enable
    def __init__(self, halos, seed=None, use_cache=False, comm=None, **params):

        from halotools.empirical_models import model_defaults

        # check type
        from halotools.sim_manager import UserSuppliedHaloCatalog
        if not isinstance(halos, UserSuppliedHaloCatalog):
            raise TypeError("input halos catalog for HOD should be halotools.sim_manager.UserSuppliedHaloCatalog")

        # try to extract meta-data from catalog
        mdef     = getattr(halos, 'mdef', 'vir')
        cosmo    = getattr(halos, 'cosmology', None)
        Lbox     = getattr(halos, 'Lbox', None)
        redshift = getattr(halos, 'redshift', None)

        # fail if we are missing any of these
        for name, attr in zip(['cosmology', 'Lbox', 'redshift'], [cosmo, Lbox, redshift]):
            if attr is None:
                raise AttributeError("input UserSuppliedHaloCatalog must have '%s attribute" %name)

        # promote astropy cosmology to nbodykit's Cosmology
        from astropy.cosmology import FLRW
        if isinstance(cosmo, FLRW):
            from nbodykit.cosmology import Cosmology
            cosmo = Cosmology.from_astropy(cosmo)

        # store the halotools catalog
        self._halos = halos
        self.cosmo  = cosmo
        self.comm   = comm

        # set the seed randomly if it is None
        if seed is None:
            if self.comm.rank == 0:
                seed = numpy.random.randint(0, 4294967295)
            seed = self.comm.bcast(seed)

        # grab the BoxSize from the halotools catalog
        self.attrs['BoxSize'] = numpy.empty(3)
        self.attrs['BoxSize'][:] = Lbox

        # store mass and radius keys
        self.mass   = model_defaults.get_halo_mass_key(mdef)
        self.radius = model_defaults.get_halo_boundary_key(mdef)

        # check for any missing columns
        needed = ['halo_%s' %s for s in ['x','y','z','vx','vy','vz', 'id', 'upid']] + [self.mass, self.radius]
        missing = set(needed) - set(halos.halo_table.colnames)
        if len(missing):
            raise ValueError("missing columns from halotools UserSuppliedHaloCatalog: %s" %str(missing))

        # this ensures that all columns in the halo catalog will propagate to the galaxy catalog
        model_defaults.default_haloprop_list_inherited_by_mock = halos.halo_table.colnames

        # store the attributes
        self.attrs['mdef'] = mdef
        self.attrs['redshift'] = redshift
        self.attrs['seed'] = seed
        self.attrs.update(params)

        # add cosmo attributes
        self.attrs['cosmo'] = dict(cosmo)

        # make the model!
        self._model = self.__makemodel__()

        # set the HOD params
        for param in self._model.param_dict:
            if param not in self.attrs:
                raise ValueError("missing '%s' parameter when initializing HOD" %param)
            self._model.param_dict[param] = self.attrs[param]

        # make the actual source
        ArrayCatalog.__init__(self, self.__makesource__(), comm=comm, use_cache=use_cache)

        # crash with no particles!
        if self.csize == 0:
            raise ValueError("no particles in catalog after populating HOD")

    @abc.abstractmethod
    def __makemodel__(self):
        """
        Abstract class to be overwritten by user; this should return
        the HOD model instance that will be used to do the mock
        population.

        See :ref:`the documentation <custom-hod-mocks>` for more details.

        Returns
        -------
        :class:`~halotools.empirical_models.HodModelFactory`
            the halotools object implementing the HOD model
        """
        pass

    def __makesource__(self):
        """
        Make the source of galaxies by performing the halo HOD population

        .. note::
            The mock population is only done by the root, and the resulting
            catalog is then distributed evenly amongst the available ranks
        """
        from astropy.table import Table

        # gather all halos to root
        halo_table = find_object_dtypes(self._halos.halo_table)
        all_halos = GatherArray(halo_table.as_array(), self.comm, root=0)

        # root does the mock population
        if self.comm.rank == 0:

            # set the halo table on the root to the Table containing all halo
            self._halos.halo_table = Table(data=all_halos, copy=True)
            del all_halos

            # populate
            self._model.populate_mock(halocat=self._halos, halo_mass_column_key=self.mass,
                                      Num_ptcl_requirement=1, seed=self.attrs['seed'])

            # remap gal_type to integers (cen: 0, sats: 1)
            gal_type_integers(self._model.mock.galaxy_table)

            # crash if any object dtypes
            data = find_object_dtypes(self._model.mock.galaxy_table).as_array()
            del self._model.mock.galaxy_table
        else:
            data = None

        # log the stats
        if self.comm.rank == 0:
            self._log_populated_stats(data)

        return ScatterArray(data, self.comm)

    def repopulate(self, seed=None, **params):
        """
        Update the HOD parameters and then re-populate the mock catalog

        .. warning::
            This operation is done in-place, so the size of the Source
            changes

        Parameters
        ----------
        seed : int, optional
            the new seed to use when populating the mock
        params :
            key/value pairs of HOD parameters to update
        """
        # set the seed randomly if it is None
        if seed is None:
            if self.comm.rank == 0:
                seed = numpy.random.randint(0, 4294967295)
            seed = self.comm.bcast(seed)
        self.attrs['seed'] = seed

        # update the HOD model parameters
        for name in params:
            if name not in self._model.param_dict:
                valid = list(self._model.param_dict.keys())
                raise ValueError("'%s' is not a valid Hod parameter name; valid are: %s" %(name, str(valid)))
            self._model.param_dict[name] = params[name]
            self.attrs[name] = params[name]

        # the root will do the mock population
        if self.comm.rank == 0:

            # re-populate the mock (without halo catalog pre-processing)
            self._model.mock.populate(Num_ptcl_requirement=1,
                                      halo_mass_column_key=self.mass,
                                      seed=self.attrs['seed'])

            # remap gal_type to integers (cen: 0, sats: 1)
            gal_type_integers(self._model.mock.galaxy_table)

            # crash if any object dtypes
            data = find_object_dtypes(self._model.mock.galaxy_table).as_array()
            del self._model.mock.galaxy_table

        else:
            data = None

        # log the stats
        if self.comm.rank == 0:
            self._log_populated_stats(data)

        # re-initialize with new source
        ArrayCatalog.__init__(self, ScatterArray(data, self.comm), comm=self.comm, use_cache=self.use_cache)

    def _log_populated_stats(self, data):
        """
        Internal function to log statistics of the populated catalog
        """
        if len(data) > 0:

            fsat = 1.*(data['gal_type'] == 1).sum()/len(data)
            self.logger.info("satellite fraction: %.2f" %fsat)
            self.attrs['fsat'] = fsat

            logmass = numpy.log10(data[self.mass])
            self.logger.info("mean log10 halo mass: %.2f" %logmass.mean())
            self.logger.info("std log10 halo mass: %.2f" %logmass.std())

    @column
    def Position(self):
        """
        Galaxy positions, in units of Mpc/h
        """
        pos = numpy.vstack([self._source['x'], self._source['y'], self._source['z']]).T
        return self.make_column(pos)

    @column
    def Velocity(self):
        """
        Galaxy velocity, in units of km/s
        """
        vel = numpy.vstack([self._source['vx'], self._source['vy'], self._source['vz']]).T
        return self.make_column(vel)

    @column
    def VelocityOffset(self):
        """
        The RSD velocity offset, in units of Mpc/h

        This multiplies Velocity by 1 / (a*100*E(z)) = 1 / (a H(z)/h)
        """
        z = self.attrs['redshift']
        rsd_factor = (1+z) / (100*self.cosmo.efunc(z))
        return self['Velocity'] * rsd_factor

class HODCatalog(HODBase):
    """
    A CatalogSource that uses the HOD prescription of Zheng et al 2007
    to populate an input halo catalog with galaxies.

    The mock population is done using :mod:`halotools`. See the documentation
    for :class:`halotools.empirical_models.Zheng07Cens` and
    :class:`halotools.empirical_models.Zheng07Sats` for further details
    regarding the HOD.

    The columns generated in this catalog are:

    #. **Position**: the galaxy position
    #. **Velocity**: the galaxy velocity
    #. **VelocityOffset**: the RSD velocity offset, in units of distance
    #. **conc_NFWmodel**: the concentration of the halo
    #. **gal_type**: the galaxy type, 0 for centrals and 1 for satellites
    #. **halo_id**: the global ID of the halo this galaxy belongs to, between 0 and :attr:`csize`
    #. **halo_local_id**: the local ID of the halo this galaxy belongs to, between 0 and :attr:`size`
    #. **halo_mvir**: the halo mass
    #. **halo_nfw_conc**: alias of ``conc_NFWmodel``
    #. **halo_num_centrals**: the number of centrals that this halo hosts, either 0 or 1
    #. **halo_num_satellites**: the number of satellites that this halo hosts
    #. **halo_rvir**: the halo radius
    #. **halo_upid**: equal to -1; should be ignored by the user
    #. **halo_vx, halo_vy, halo_vz**: the three components of the halo velocity
    #. **halo_x, halo_y, halo_z**: the three components of the halo position
    #. **host_centric_distance**: the distance from this galaxy to the center of the halo
    #. **vx, vy, vz**: the three components of the galaxy velocity, equal to ``Velocity``
    #. **x,y,z**: the three components of the galaxy position, equal to ``Position``

    For futher details, please see the :ref:`documentation <hod-mock-data>`.

    .. note::
         Default HOD values are from
         `Reid et al. 2014 <https://arxiv.org/abs/1404.3742>`_

    Parameters
    ----------
    halos : :class:`~halotools.sim_manager.UserSuppliedHaloCatalog`
        the halotools table holding the halo data; this object must have
        the following attributes: `cosmology`, `Lbox`, `redshift`
    logMmin : float, optional
        Minimum mass required for a halo to host a central galaxy
    sigma_logM : float, optional
        Rate of transition from <Ncen>=0 --> <Ncen>=1
    alpha : float, optional
        Power law slope of the relation between halo mass and <Nsat>
    logM0 : float, optional
        Low-mass cutoff in <Nsat>
    logM1 : float, optional
        Characteristic halo mass where <Nsat> begins to assume a power law form
    seed : int, optional
        the random seed to generate deterministic mocks

    References
    ----------
    `Zheng et al. (2007), arXiv:0703457 <https://arxiv.org/abs/astro-ph/0703457>`_
    """
    logger = logging.getLogger("HOD")

    @CurrentMPIComm.enable
    def __init__(self, halos, logMmin=13.031, sigma_logM=0.38,
                    alpha=0.76, logM0=13.27, logM1=14.08,
                    seed=None, use_cache=False, comm=None):

        params = {}
        params['logMmin'] = logMmin
        params['sigma_logM'] = sigma_logM
        params['alpha'] = alpha
        params['logM0'] = logM0
        params['logM1'] = logM1

        HODBase.__init__(self, halos, seed=seed, use_cache=use_cache, comm=comm, **params)

    def __repr__(self):
        names = ['logMmin', 'sigma_logM', 'alpha', 'logM0', 'logM1']
        s = ', '.join(['%s=%.2f' %(k,self.attrs[k]) for k in names])
        return "HODCatalog(%s)" %s

    def __makemodel__(self):
        """
        Return the Zheng 07 HOD model.

        This model evaluates Eqs. 2 and 5 of Zheng et al. 2007
        """
        from halotools.empirical_models import HodModelFactory
        from halotools.empirical_models import Zheng07Sats, Zheng07Cens
        from halotools.empirical_models import NFWPhaseSpace, TrivialPhaseSpace

        model = {}

        # use concentration from halo table
        if 'halo_nfw_conc' in self._halos.halo_table.colnames:
            conc_mass_model = 'direct_from_halo_catalog'
        # use empirical prescription for c(M)
        else:
            conc_mass_model = 'dutton_maccio14'

        # occupation functions
        cenocc = Zheng07Cens(prim_haloprop_key=self.mass)
        satocc = Zheng07Sats(prim_haloprop_key=self.mass, modulate_with_cenocc=True, cenocc_model=cenocc)
        satocc._suppress_repeated_param_warning = True

        # add to model
        model['centrals_occupation'] = cenocc
        model['satellites_occupation'] = satocc

        # profile functions
        kws = {'cosmology':self.cosmo.to_astropy(), 'redshift':self.attrs['redshift'], 'mdef':self.attrs['mdef']}
        model['centrals_profile'] = TrivialPhaseSpace(**kws)
        model['satellites_profile'] = NFWPhaseSpace(conc_mass_model=conc_mass_model, **kws)

        return HodModelFactory(**model)
