import numpy
import logging

import kdcount
from nbodykit import CurrentMPIComm
from nbodykit.binned_statistic import BinnedStatistic
from pmesh.domain import GridND
from nbodykit.utils import split_size_3d

class Multipoles3PCF(object):
    """
    Compute the multipoles of the isotropic, three-point correlation function
    in configuration space.

    This uses the algorithm of Slepian and Eisenstein, 2015 which scales
    as :math:`\mathcal{O}(N^2)`, where :math:`N` is the number of objects.

    Results are computed when the object is inititalized. See the documenation
    of :func:`~Multipoles3PCF.run` for the attributes storing the results.

    Parameters
    ----------
    source : CatalogSource
        the input source of particles providing the 'Position' column
    poles : list of int
        the list of multipole numbers to compute
    edges : array_like
        the edges of the bins of separation to use; length of nbins+1
    BoxSize : float, 3-vector, optional
        the size of the box; if periodic boundary conditions used, and 'BoxSize'
        not provided in the source :attr:`attrs`, it must be provided here
    periodic : bool, optional
        whether to use periodic boundary conditions when computing separations
        between objects
    weight : str, optional
        the name of the column in the source specifying the particle weights
    selection : str, optional
        if not ``None``, the name of the column to use to select certain objects;
        should be the name of a boolean column

    References
    ----------
    Slepian and Eisenstein, MNRAS 454, 4142-4158 (2015)
    """
    logger = logging.getLogger('Multipoles3PCF')

    def __init__(self, source, poles, edges, BoxSize=None, periodic=True,
                 weight='Weight', selection='Selection'):

        # check for all of the necessary columns
        for col in ['Position', weight, selection]:
            if col not in source:
                raise ValueError("the '%s' column must be defined in the source" %col)

        # store the subset of the source we selected
        self.source = source[source[selection]]
        self.comm = source.comm
        self.attrs = {}

        # need BoxSize
        self.attrs['BoxSize'] = numpy.empty(3)
        BoxSize = source.attrs.get('BoxSize', BoxSize)
        if periodic and BoxSize is None:
            raise ValueError("please specify a BoxSize if using periodic boundary conditions")
        self.attrs['BoxSize'][:] = BoxSize

        # test rmax for PBC
        if periodic and numpy.amax(edges) > 0.5*self.attrs['BoxSize'].min():
            raise ValueError("periodic pair counts cannot be computed for Rmax > 0.5 * BoxSize")

        # save meta-data
        self.attrs['edges'] = edges
        self.attrs['poles'] = poles
        self.attrs['periodic'] = periodic
        self.attrs['weight'] = weight
        self.attrs['selection'] = selection

        self.run()

    def run(self):
        """
        Compute the three-point CF multipoles. This attaches the following
        the attributes to the class:

        - :attr:`poles`

        Attributes
        ----------
        poles : :class:`~nbodykit.binned_statistic.BinnedStatistic`
            a BinnedStatistic object to hold the multipole results; the
            binned statistics stores the multipoles as variables ``zeta_0``,
            ``zeta_1``, etc for :math:`\ell=0,1,` etc. The coordinates
            of the binned statistic are ``r1`` and ``r2``, which give the
            separations between the three objects in CF
        """
        redges = self.attrs['edges']
        comm   = self.comm
        nbins  = len(redges)-1
        Nell   = len(self.attrs['poles'])

        if self.attrs['periodic']:
            boxsize = self.attrs['BoxSize']
        else:
            boxsize = None

        # determine processor division for domain decomposition
        np = split_size_3d(comm.size)
        if self.comm.rank == 0:
            self.logger.info("using cpu grid decomposition: %s" %str(np))

        # output zeta
        zeta = numpy.zeros((Nell,nbins,nbins), dtype='f8')

        # compute the Ylm expressions we need
        if self.comm.rank == 0:
            self.logger.info("computing Ylm expressions...")
        Ylm_cache = YlmCache(self.attrs['poles'], comm)
        if self.comm.rank ==  0:
            self.logger.info("...done")

        # get the (periodic-enforced) position
        pos = self.source['Position']
        if self.attrs['periodic']:
            pos %= self.attrs['BoxSize']
        pos, w = self.source.compute(pos, self.source[self.attrs['weight']])

        # global min/max across all ranks
        posmin = numpy.asarray(comm.allgather(pos.min(axis=0))).min(axis=0)
        posmax = numpy.asarray(comm.allgather(pos.max(axis=0))).max(axis=0)

        # domain decomposition
        grid = [numpy.linspace(posmin[i], posmax[i], np[i]+1, endpoint=True) for i in range(3)]
        domain = GridND(grid, comm=comm)

        layout = domain.decompose(pos, smoothing=0)
        pos    = layout.exchange(pos)
        w      = layout.exchange(w)

        # get the position/weight of the secondaries
        rmax = numpy.max(self.attrs['edges'])
        if rmax > self.attrs['BoxSize'].max() * 0.25:
            pos_sec = numpy.concatenate(comm.allgather(pos), axis=0)
            w_sec   = numpy.concatenate(comm.allgather(w), axis=0)
        else:
            layout  = domain.decompose(pos, smoothing=rmax)
            pos_sec = layout.exchange(pos)
            w_sec   = layout.exchange(w)

        # make the KD-tree holding the secondaries
        tree_sec = kdcount.KDTree(pos_sec, boxsize=boxsize).root

        def callback(r, i, j, iprim=None):

            # remove self pairs
            valid = r > 0.
            r = r[valid]; i = i[valid]

            if iprim % 100 == 0 and self.comm.rank == 0:
                self.logger.info("done %d centrals" %iprim)

            # normalized, re-centered position array (periodic)
            dpos = (pos_sec[i] - pos[iprim])

            # enforce periodicity in dpos
            if self.attrs['periodic']:
                for axis, col in enumerate(dpos.T):
                    col[col > boxsize[axis]*0.5] -= boxsize[axis]
                    col[col <= -boxsize[axis]*0.5] += boxsize[axis]
            recen_pos = dpos / r[:,numpy.newaxis]

            # find the mapping of r to rbins
            dig = numpy.searchsorted(self.attrs['edges'], r, side='left')

            # evaluate all Ylms
            Ylms = Ylm_cache(recen_pos[:,0]+1j*recen_pos[:,1], recen_pos[:,2])

            # sqrt of primary weight
            w0 = w[iprim]

            # loop over each (l,m) pair
            for (l,m) in Ylms:

                # the Ylm evaluated at galaxy positions
                weights = Ylms[(l,m)] * w_sec[i]

                # sum over for each radial bin
                alm = numpy.zeros(nbins, dtype='c8')
                alm += numpy.bincount(dig, weights=weights.real, minlength=nbins+2)[1:-1]
                if m != 0:
                    alm += 1j*numpy.bincount(dig, weights=weights.imag, minlength=nbins+2)[1:-1]

                # compute alm * conjugate(alm)
                alm = w0*numpy.outer(alm, alm.conj())
                if m != 0: alm += alm.T # add in the -m contribution for m != 0
                zeta[l,...] += alm.real

        # compute multipoles for each primary
        for iprim in range(len(pos)):
            tree_prim = kdcount.KDTree(numpy.atleast_2d(pos[iprim]), boxsize=boxsize).root
            tree_sec.enum(tree_prim, rmax, process=callback, iprim=iprim)

        # sum across all ranks
        zeta = comm.allreduce(zeta)

        # normalize according to Eq. 15 of Slepian et al. 2015
        # differs by factor of (4 pi)^2 / (2l+1) from the C++ code
        zeta /= (4*numpy.pi)

        # make a BinnedStatistic
        dtype = numpy.dtype([('zeta_%d' %i, zeta.dtype) for i in range(Nell)])
        data = numpy.empty(zeta.shape[-2:], dtype=dtype)
        for i in range(Nell):
            data['zeta_%d' %i] = zeta[i]

        # save the result
        self.poles = BinnedStatistic(['r1', 'r2'], [redges, redges], data)

    def __getstate__(self):
        return {'poles':self.poles.data, 'attrs':self.attrs}

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.poles = BinnedStatistic(['r1', 'r2'], [self.attrs['edges']]*2, self.poles)

    def save(self, output):
        """
        Save the :attr:`poles` result to a JSON file with name ``output``
        """
        import json
        from nbodykit.utils import JSONEncoder

        # only the master rank writes
        if self.comm.rank == 0:
            self.logger.info('measurement done; saving result to %s' % output)

            with open(output, 'w') as ff:
                json.dump(self.__getstate__(), ff, cls=JSONEncoder)

    @classmethod
    @CurrentMPIComm.enable
    def load(cls, filename, comm=None):
        """
        Load a Multipoles3PCF result from ``filename`` that has been saved to
        disk with :func:`~Multipoles3PCF.save`.
        """
        import json
        from nbodykit.utils import JSONDecoder
        if comm.rank == 0:
            with open(filename, 'r') as ff:
                state = json.load(ff, cls=JSONDecoder)
        else:
            state = None
        state = comm.bcast(state)
        self = object.__new__(cls)
        self.__setstate__(state)
        self.comm = comm
        return self

class YlmCache(object):
    """
    A class to compute spherical harmonics :math:`Y_{lm}` up
    to a specified maximum :math:`\ell`

    During calculation, the necessary power of Cartesian unit
    vectors are cached in memory to avoid repeated calculations
    for separate harmonics.
    """
    def __init__(self, ells, comm):

        import sympy as sp
        from sympy.utilities.lambdify import implemented_function
        from sympy.parsing.sympy_parser import parse_expr

        self.ells = list(ells)
        self.max_ell = max(ells)
        lms = [(int(l),int(m)) for l in ells for m in range(0, l+1)]

        # compute the Ylm string expressions in parallel
        exprs = []
        for i in range(comm.rank, len(lms), comm.size):
            lm = lms[i]
            exprs.append((lm, str(self._get_Ylm(*lm))))
        exprs = [x for sublist in comm.allgather(exprs) for x in sublist]

        # determine the powers entering into each expression
        args = {}
        for lm, expr in exprs:
            matches = []
            for var in ['xpyhat', 'zhat']:
                for e in range(2, max(ells)+1):
                    name = var + '**' + str(e)
                    if name in expr:
                        matches.append((name, 'cached_'+var, str(e)))
                args[lm] = matches


        # define a function to return cached power
        def from_cache(name, pow):
            return self._cache[str(name)+str(pow)]
        f = implemented_function(sp.Function('from_cache'), from_cache)

        # arguments to the sympy functions
        zhat   = sp.Symbol('zhat', real=True, positive=True)
        xpyhat = sp.Symbol('xpyhat', complex=True)

        self._cache = {}

        # make the Ylm functions
        self._Ylms = {}
        for lm, expr in exprs:
            expr = parse_expr(expr, local_dict={'zhat':zhat, 'xpyhat':xpyhat})
            for var in args[lm]:
                expr = expr.replace(var[0], 'from_cache(%s, %s)' %var[1:])
            self._Ylms[lm] = sp.lambdify((xpyhat, zhat), expr)

    def __call__(self, xpyhat, zhat):
        """
        Return a dictionary holding Ylm for each (l,m) combination
        required

        Parameters
        ----------
        xpyhat : array_like
            a complex array holding xhat + i * yhat, where xhat and yhat
            are the two cartesian unit vectors
        zhat : array_like
            the third cartesian unit vector
        """
        # fill the cache first
        self._cache['cached_xpyhat2'] = xpyhat**2
        self._cache['cached_zhat2'] = zhat**2
        for name,x in zip(['cached_xpyhat', 'cached_zhat'], [xpyhat, zhat]):
            for i in range(3, self.max_ell+1):
                self._cache[name+str(i)] = self._cache[name+str(i-1)]*x

        # return a dictionary for each (l,m) tuple
        toret = {}
        for lm in self._Ylms:
            toret[lm] = self._Ylms[lm](xpyhat, zhat)
        return toret

    def _get_Ylm(self, l, m):
        """
        Compute an expression for spherical harmonic of order (l,m)
        in terms of Cartesian unit vectors, :math:`\hat{z}`
        and :math:`\hat{x} + i \hat{y}`

        Parameters
        ----------
        l : int
            the degree of the harmonic
        m : int
            the order of the harmonic; |m| < l

        Returns
        -------
        expr :
            a sympy expression that corresponds to the
            requested Ylm

        References
        ----------
        https://en.wikipedia.org/wiki/Spherical_harmonics
        """
        import sympy as sp

        # the relevant cartesian and spherical symbols
        x, y, z, r = sp.symbols('x y z r', real=True, positive=True)
        xhat, yhat, zhat = sp.symbols('xhat yhat zhat', real=True, positive=True)
        xpyhat = sp.Symbol('xpyhat', complex=True)
        phi, theta = sp.symbols('phi theta')
        defs = [(sp.sin(phi), y/sp.sqrt(x**2+y**2)),
                (sp.cos(phi), x/sp.sqrt(x**2+y**2)),
                (sp.cos(theta), z/sp.sqrt(x**2 + y**2 + z**2))
                ]

        # the cos(theta) dependence encoded by the associated Legendre poly
        expr = sp.assoc_legendre(l, m, sp.cos(theta))

        # the exp(i*m*phi) dependence
        expr *= sp.expand_trig(sp.cos(m*phi)) + sp.I*sp.expand_trig(sp.sin(m*phi))

        # simplifying optimizations
        expr = sp.together(expr.subs(defs)).subs(x**2 + y**2 + z**2, r**2)
        expr = expr.expand().subs([(x/r, xhat), (y/r, yhat), (z/r, zhat)])
        expr = expr.factor().factor(extension=[sp.I]).subs(xhat+sp.I*yhat, xpyhat)
        expr = expr.subs(xhat**2 + yhat**2, 1-zhat**2).factor()

        # and finally add the normalization
        amp = sp.sqrt((2*l+1) / (4*numpy.pi) * sp.factorial(l-m) / sp.factorial(l+m))
        expr *= amp

        return expr
