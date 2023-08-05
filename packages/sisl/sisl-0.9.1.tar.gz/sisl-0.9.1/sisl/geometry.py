from __future__ import print_function, division

# To check for integers
import warnings
from numbers import Integral, Real
from six import string_types
from math import acos
from itertools import product

import numpy as np

import sisl._plot as plt
import sisl._array as _a
import sisl.linalg as lin

from ._help import _str
from ._help import _range as range
from ._help import ensure_array, ensure_dtype
from ._help import isndarray
from .utils import default_ArgumentParser, default_namespace, cmd
from .utils import angle, direction
from .utils import lstranges, strmap, array_arange
from .quaternion import Quaternion
from .supercell import SuperCell, SuperCellChild
from .atom import Atom, Atoms
from .shape import Shape, Sphere, Cube
from .sparse_geometry import SparseAtom

__all__ = ['Geometry', 'sgeom']


class Geometry(SuperCellChild):
    """ Holds atomic information, coordinates, species, lattice vectors

    The `Geometry` class holds information regarding atomic coordinates,
    the atomic species, the corresponding lattice-vectors.

    It enables the interaction and conversion of atomic structures via
    simple routine methods.

    All lengths are assumed to be in units of Angstrom, however, as
    long as units are kept same the exact units are irrespective.

    .. code::

       >>> square = Geometry([[0.5, 0.5, 0.5]], Atom(1),
       ...                   sc=SuperCell([1, 1, 10], nsc=[3, 3, 1]))
       >>> print(square)
       Geometry{na: 1, no: 1,
        Atoms{species: 1,
          Atom{H, Z: 1, orbs: 1, mass(au): 1.00794, maxR: -1.00000}: 1, 
        },
        nsc: [3, 3, 1], maxR: -1.0
       }


    Attributes
    ----------
    na : int
        number of atoms, ``len(self)``
    xyz : ndarray
        atomic coordinates
    atom : Atoms
        the atomic objects associated with each atom (indexable)
    sc : SuperCell
        the supercell describing the periodicity of the
        geometry
    no: int
        total number of orbitals in the geometry
    maxR : float np.max([a.maxR() for a in self.atom])
        maximum orbital range

    Parameters
    ----------
    xyz : array_like
        atomic coordinates
        ``xyz[i, :]`` is the atomic coordinate of the i'th atom.
    atom : array_like or Atoms
        atomic species retrieved from the `PeriodicTable`
    sc : SuperCell
        the unit-cell describing the atoms in a periodic
        super-cell

    Examples
    --------

    An atomic lattice consisting of Hydrogen atoms.
    An atomic square lattice of Hydrogen atoms

    >>> xyz = [[0, 0, 0],
    ...        [1, 1, 1]]
    >>> sc = SuperCell([2,2,2])
    >>> g = Geometry(xyz, Atom('H'), sc)

    The following estimates the lattice vectors from the
    atomic coordinates, although possible, it is not recommended
    to be used.

    >>> xyz = [[0, 0, 0],
    ...        [1, 1, 1]]
    >>> g = Geometry(xyz, Atom('H'))

    See Also
    --------
    Atoms : contained atoms `self.atom`
    Atom : contained atoms are each an object of this
    """

    def __init__(self, xyz, atom=None, sc=None):

        # Create the geometry coordinate
        self.xyz = np.copy(np.asarray(xyz, dtype=np.float64))
        self.xyz.shape = (-1, 3)

        # Default value
        if atom is None:
            atom = Atom('H')

        # Create the local Atoms object
        self._atom = Atoms(atom, na=self.na)

        self.__init_sc(sc)

    def __init_sc(self, sc):
        """ Initializes the supercell by *calculating* the size if not supplied

        If the supercell has not been passed we estimate the unit cell size
        by calculating the bond-length in each direction for a square
        Cartesian coordinate system.
        """
        # We still need the *default* super cell for
        # estimating the supercell
        self.set_supercell(sc)

        if sc is not None:
            return

        # First create an initial guess for the supercell
        # It HAS to be VERY large to not interact
        closest = self.close(0, R=(0., 0.4, 5.))[2]
        if len(closest) < 1:
            # We could not find any atoms very close,
            # hence we simply return and now it becomes
            # the users responsibility

            # We create a molecule box with +10 A in each direction
            m, M = np.amin(self.xyz, axis=0), np.amax(self.xyz, axis=0) + 10.
            self.set_supercell(M-m)
            return

        sc_cart = np.zeros([3], np.float64)
        cart = np.zeros([3], np.float64)
        for i in range(3):
            # Initialize cartesian direction
            cart[i] = 1.

            # Get longest distance between atoms
            max_dist = np.amax(self.xyz[:, i]) - np.amin(self.xyz[:, i])

            dist = self.xyz[closest, :] - self.xyz[0, :][None, :]
            # Project onto the direction
            dd = np.abs(np.dot(dist, cart))

            # Remove all below .4
            tmp_idx = (dd >= .4).nonzero()[0]
            if len(tmp_idx) > 0:
                # We have a success
                # Add the bond-distance in the Cartesian direction
                # to the maximum distance in the same direction
                sc_cart[i] = max_dist + np.amin(dd[tmp_idx])
            else:
                # Default to LARGE array so as no
                # interaction occurs (it may be 2D)
                sc_cart[i] = max(10., max_dist)
            cart[i] = 0.

        # Re-set the supercell to the newly found one
        self.set_supercell(sc_cart)

    @property
    def atom(self):
        """ Atoms for the geometry (`Atoms` object) """
        return self._atom

    # Backwards compatability (do not use)
    atoms = atom

    def maxR(self, all=False):
        """ Maximum orbital range of the atoms """
        return self.atom.maxR(all)

    @property
    def na(self):
        """ Number of atoms in geometry """
        return self.xyz.shape[0]

    @property
    def na_s(self):
        """ Number of supercell atoms """
        return self.na * self.n_s

    def __len__(self):
        """ Number of atoms in geometry """
        return self.na

    @property
    def no(self):
        """ Number of orbitals """
        return self.atom.no

    @property
    def no_s(self):
        """ Number of supercell orbitals """
        return self.no * self.n_s

    @property
    def firsto(self):
        """ The first orbital on the corresponding atom """
        return self.atom.firsto

    @property
    def lasto(self):
        """ The last orbital on the corresponding atom """
        return self.atom.lasto

    @property
    def orbitals(self):
        """ List of orbitals per atom """
        return self.atom.orbitals

    ## End size of geometry

    def __getitem__(self, atom):
        """ Geometry coordinates (allows supercell indices) """
        if isinstance(atom, Integral):
            return self.axyz(atom)

        elif isinstance(atom, slice):
            if atom.stop is None:
                atom = atom.indices(self.na)
            else:
                atom = atom.indices(self.na_s)
            return self.axyz(np.arange(atom[0], atom[1], atom[2], dtype=np.int32))

        elif atom is None:
            return self.axyz()

        elif isinstance(atom, tuple):
            return self[atom[0]][..., atom[1]]

        elif atom[0] is None:
            return self.axyz()[:, atom[1]]

        return self.axyz(atom)

    def reorder(self):
        """ Reorders atoms according to first occurence in the geometry

        Notes
        -----
        This is an in-place operation.
        """
        self._atom = self._atom.reorder()

    def reduce(self):
        """ Remove all atoms not currently used in the ``self.atom`` object

        Notes
        -----
        This is an in-place operation.
        """
        self._atom = self._atom.reduce()

    def rij(self, ia, ja):
        r""" Distance between atom `ia` and `ja`, atoms can be in super-cell indices

        Returns the distance between two atoms:

        .. math::
            r_{ij} = |r_j - r_i|

        Parameters
        ----------
        ia : int or array_like
           atomic index of first atom
        ja : int or array_like
           atomic indices
        """
        R = self.Rij(ia, ja)

        if len(R.shape) == 1:
            return (R[0] ** 2. + R[1] ** 2 + R[2] ** 2) ** .5

        return np.sqrt(np.sum(R ** 2, axis=1))

    def Rij(self, ia, ja):
        r""" Vector between atom `ia` and `ja`, atoms can be in super-cell indices

        Returns the vector between two atoms:

        .. math::
            R_{ij} = r_j - r_i

        Parameters
        ----------
        ia : int or array_like
           atomic index of first atom
        ja : int or array_like
           atomic indices
        """
        xi = self.axyz(ia)
        xj = self.axyz(ja)

        if isinstance(ja, Integral):
            return xj[:] - xi[:]
        elif np.all(xi.shape == xj.shape):
            return xj - xi

        return xj - xi[None, :]

    def orij(self, io, jo):
        r""" Distance between orbital `io` and `jo`, orbitals can be in super-cell indices

        Returns the distance between two orbitals:

        .. math::
            r_{ij} = |r_j - r_i|

        Parameters
        ----------
        io : int or array_like
           orbital index of first orbital
        jo : int or array_like
           orbital indices
        """
        return self.rij(self.o2a(io), self.o2a(jo))

    def oRij(self, io, jo):
        r""" Vector between orbital `io` and `jo`, orbitals can be in super-cell indices

        Returns the vector between two orbitals:

        .. math::
            R_{ij} = r_j - r_i

        Parameters
        ----------
        io : int or array_like
           orbital index of first orbital
        jo : int or array_like
           orbital indices
        """
        return self.Rij(self.o2a(io), self.o2a(jo))

    @staticmethod
    def read(sile, *args, **kwargs):
        """ Reads geometry from the `Sile` using `Sile.read_geometry`

        Parameters
        ----------
        sile : `Sile`, str
            a `Sile` object which will be used to read the geometry
            if it is a string it will create a new sile using `get_sile`.

        See Also
        --------
        write : writes a `Geometry` to a given `Sile`/file
        """
        # This only works because, they *must*
        # have been imported previously
        from sisl.io import get_sile, BaseSile
        if isinstance(sile, BaseSile):
            return sile.read_geometry(*args, **kwargs)
        else:
            with get_sile(sile) as fh:
                return fh.read_geometry(*args, **kwargs)

    def write(self, sile, *args, **kwargs):
        """ Writes geometry to the `Sile` using `sile.write_geometry`

        Parameters
        ----------
        sile : ``Sile``, ``str``
            a `Sile` object which will be used to write the geometry
            if it is a string it will create a new sile using `get_sile`
        *args, **kwargs:
            Any other args will be passed directly to the
            underlying routine

        See Also
        --------
        read : reads a `Geometry` from a given `Sile`/file
        """
        # This only works because, they *must*
        # have been imported previously
        from sisl.io import get_sile, BaseSile
        if isinstance(sile, BaseSile):
            sile.write_geometry(self, *args, **kwargs)
        else:
            with get_sile(sile, 'w') as fh:
                fh.write_geometry(self, *args, **kwargs)

    def __repr__(self):
        """ Representation of the object """
        s = self.__class__.__name__ + '{{na: {0}, no: {1},\n '.format(self.na, self.no)
        s += repr(self.atom).replace('\n', '\n ')
        return (s[:-2] + ',\n nsc: [{1}, {2}, {3}], maxR: {0}\n}}\n'.format(self.maxR(), *self.nsc)).strip()

    def iter(self):
        """ An iterator over all atomic indices

        This iterator is the same as:

        >>> for ia in range(len(self)): # doctest: +SKIP
        ...    <do something> # doctest: +SKIP

        or equivalently

        >>> for ia in self: # doctest: +SKIP
        ...    <do something> # doctest: +SKIP

        See Also
        --------
        iter_species : iterate across indices and atomic species
        iter_orbitals : iterate across atomic indices and orbital indices
        """
        for ia in range(len(self)):
            yield ia

    __iter__ = iter

    def iter_species(self, atom=None):
        """ Iterator over all atoms (or a subset) and species as a tuple in this geometry

        >>> for ia, a, idx_specie in self.iter_species(): # doctest: +SKIP
        ...     isinstance(ia, int) == True # doctest: +SKIP
        ...     isinstance(a, Atom) == True # doctest: +SKIP
        ...     isinstance(idx_specie, int) == True # doctest: +SKIP

        with ``ia`` being the atomic index, ``a`` the `Atom` object, `idx_specie`
        is the index of the specie

        Parameters
        ----------
        atom : int or array_like, optional
           only loop on the given atoms, default to all atoms

        See Also
        --------
        iter : iterate over atomic indices
        iter_orbitals : iterate across atomic indices and orbital indices
        """
        if atom is None:
            for ia in self:
                yield ia, self.atom[ia], self.atom.specie[ia]
        else:
            for ia in ensure_array(atom):
                yield ia, self.atom[ia], self.atom.specie[ia]

    def iter_orbitals(self, atom=None, local=True):
        """
        Returns an iterator over all atoms and their associated orbitals

        >>> for ia, io in self.iter_orbitals(): # doctest: +SKIP

        with ``ia`` being the atomic index, ``io`` the associated orbital index on atom ``ia``.
        Note that ``io`` will start from ``0``.

        Parameters
        ----------
        atom : int or array_like, optional
           only loop on the given atoms, default to all atoms
        local : bool, optional
           whether the orbital index is the global index, or the local index relative to
           the atom it resides on.

        See Also
        --------
        iter : iterate over atomic indices
        iter_species : iterate across indices and atomic species
        """
        if atom is None:
            if local:
                for ia, IO in enumerate(zip(self.firsto, self.lasto + 1)):
                    for io in range(IO[1] - IO[0]):
                        yield ia, io
            else:
                for ia, IO in enumerate(zip(self.firsto, self.lasto + 1)):
                    for io in range(IO[0], IO[1]):
                        yield ia, io
        else:
            atom = ensure_array(atom)
            if local:
                for ia, io1, io2 in zip(atom, self.firsto[atom], self.lasto[atom] + 1):
                    for io in range(io2 - io1):
                        yield ia, io
            else:
                for ia, io1, io2 in zip(atom, self.firsto[atom], self.lasto[atom] + 1):
                    for io in range(io1, io2):
                        yield ia, io

    def iR(self, na=1000, iR=20, R=None):
        """ Return an integer number of maximum radii (``self.maxR()``) which holds approximately `na` atoms

        Parameters
        ----------
        na : int, optional
           number of atoms within the radius
        iR : int, optional
           initial `iR` value, which the sphere is estitametd from
        R : float, optional
           the value used for atomic range (defaults to ``self.maxR()``)
        """
        ia = np.random.randint(len(self))

        # default block iterator
        if R is None:
            R = self.maxR()
        if R < 0:
            raise ValueError("Unable to determine a number of atoms within a sphere with negative radius, is maxR() defined?")

        # Number of atoms within 20 * R
        naiR = max(1, len(self.close(ia, R=R * iR)))

        # Convert to na atoms spherical radii
        iR = int(4 / 3 * np.pi * R ** 3 / naiR * na)

        return iR

    def iter_block_rand(self, iR=20, R=None, atom=None):
        """ Perform the *random* block-iteration by randomly selecting the next center of block """

        # We implement yields as we can then do nested iterators
        # create a boolean array
        na = len(self)
        not_passed = np.empty(na, dtype='b')
        if atom is not None:
            # Reverse the values
            not_passed[:] = False
            not_passed[atom] = True
        else:
            not_passed[:] = True

        # Figure out how many we need to loop on
        not_passed_N = np.sum(not_passed)

        if R is None:
            R = self.maxR()
        # The boundaries (ensure complete overlap)
        R = np.array([iR - 0.975, iR + .025]) * R

        append = np.append

        # loop until all passed are true
        while not_passed_N > 0:

            # Take a random non-passed element
            all_true = not_passed.nonzero()[0]

            # Shuffle should increase the chance of hitting a
            # completely "fresh" segment, thus we take the most
            # atoms at any single time.
            # Shuffling will cut down needed iterations.
            np.random.shuffle(all_true)
            idx = all_true[0]
            del all_true

            # Now we have found a new index, from which
            # we want to create the index based stuff on

            # get all elements within two radii
            all_idx = self.close(idx, R=R)

            # Get unit-cell atoms
            all_idx[0] = self.sc2uc(all_idx[0], uniq=True)
            # First extend the search-space (before reducing)
            all_idx[1] = self.sc2uc(append(all_idx[1], all_idx[0]), uniq=True)

            # Only select those who have not been runned yet
            all_idx[0] = all_idx[0][not_passed[all_idx[0]].nonzero()[0]]
            if len(all_idx[0]) == 0:
                raise ValueError('Internal error, please report to the developers')

            # Tell the next loop to skip those passed
            not_passed[all_idx[0]] = False
            # Update looped variables
            not_passed_N -= len(all_idx[0])

            # Now we want to yield the stuff revealed
            # all_idx[0] contains the elements that should be looped
            # all_idx[1] contains the indices that can be searched
            yield all_idx[0], all_idx[1]

        if np.any(not_passed):
            raise ValueError('Error on iterations. Not all atoms has been visited.')

    def iter_block_shape(self, shape=None, iR=20, atom=None):
        """ Perform the *grid* block-iteration by looping a grid """

        # We implement yields as we can then do nested iterators
        # create a boolean array
        na = len(self)
        not_passed = np.empty(na, dtype='b')
        if atom is not None:
            # Reverse the values
            not_passed[:] = False
            not_passed[atom] = True
        else:
            not_passed[:] = True

        # Figure out how many we need to loop on
        not_passed_N = np.sum(not_passed)

        R = self.maxR()
        if shape is None:
            # we default to the Cube shapes
            dS = (Cube(R * (iR - 1.975)),
                  Cube(R * (iR + 0.025)))
        else:
            dS = tuple(shape)
            if len(dS) == 1:
                dS += dS[0].expand(R)
        if len(dS) != 2:
            raise ValueError('Number of Shapes *must* be one or two')

        # Now create the Grid
        # convert the radius to a square Grid
        # We do this by examining the x, y, z coordinates
        xyz_m = np.amin(self.xyz, axis=0)
        xyz_M = np.amax(self.xyz, axis=0)
        dxyz = xyz_M - xyz_m

        # Retrieve the internal diameter
        ir = dS[0].displacement

        # Figure out number of segments in each iteration
        # (minimum 1)
        ixyz = np.array(np.ceil(dxyz / ir + 0.0001), np.int32)

        # Calculate the steps required for each iteration
        for i in [0, 1, 2]:
            dxyz[i] = dxyz[i] / ixyz[i]

            # Correct the initial position to offset the initial displacement
            # so that we are at the border.
            xyz_m[i] += min(dxyz[i], ir[i]) / 2

            if xyz_m[i] > xyz_M[i]:
                # This is the case where one of the cell dimensions
                # is far too great.
                # In this case ixyz[i] should be 1
                xyz_m[i] = (xyz_M[i] - xyz_m[i]) / 2

        # Shorthand function
        where = np.where
        append = np.append

        # Now we loop in each direction
        for x, y, z in product(range(ixyz[0]),
                               range(ixyz[1]),
                               range(ixyz[2])):

            # Create the new center
            center = xyz_m + [x * dxyz[0], y * dxyz[1], z * dxyz[2]]
            # Correct in case the iteration steps across the maximum
            center = where(center < xyz_M, center, xyz_M)
            dS[0].set_center(center[:])
            dS[1].set_center(center[:])

            # Now perform the iteration
            # get all elements within two radii
            all_idx = self.within(dS)

            # Get unit-cell atoms
            all_idx[0] = self.sc2uc(all_idx[0], uniq=True)
            # First extend the search-space (before reducing)
            all_idx[1] = self.sc2uc(append(all_idx[1], all_idx[0]), uniq=True)

            # Only select those who have not been runned yet
            all_idx[0] = all_idx[0][not_passed[all_idx[0]].nonzero()[0]]
            if len(all_idx[0]) == 0:
                continue

            # Tell the next loop to skip those passed
            not_passed[all_idx[0]] = False
            # Update looped variables
            not_passed_N -= len(all_idx[0])

            # Now we want to yield the stuff revealed
            # all_idx[0] contains the elements that should be looped
            # all_idx[1] contains the indices that can be searched
            yield all_idx[0], all_idx[1]

        if np.any(not_passed):
            print(not_passed.nonzero()[0])
            print(np.sum(not_passed), len(self))
            raise ValueError('Error on iterations. Not all atoms has been visited.')

    def iter_block(self, iR=20, R=None, atom=None, method='rand'):
        """ Iterator for performance critical loops

        NOTE: This requires that `R` has been set correctly as the maximum interaction range.

        I.e. the loop would look like this:

        >>> for ias, idxs in self.iter_block(): # doctest: +SKIP
        ...    for ia in ias: # doctest: +SKIP
        ...        idx_a = self.close(ia, R = R, idx = idxs) # doctest: +SKIP

        This iterator is intended for systems with more than 1000 atoms.

        Remark that the iterator used is non-deterministic, i.e. any two iterators need
        not return the same atoms in any way.

        Parameters
        ----------
        iR  : int, optional
            the number of `R` ranges taken into account when doing the iterator
        R  : float, optional
            enables overwriting the local R quantity. Defaults to ``self.maxR()``
        atom : array_like, optional
            enables only effectively looping a subset of the full geometry
        method : {'rand', 'sphere', 'cube'}
            select the method by which the block iteration is performed.
            Possible values are:

             `rand`: a spherical object is constructed with a random center according to the internal atoms
             `sphere`: a spherical equispaced shape is constructed and looped
             `cube`: a cube shape is constructed and looped

        Returns
        -------
        Two lists with ``[0]`` being a list of atoms to be looped and ``[1]`` being the atoms that
        need searched.
        """
        method = method.lower()
        if method == 'rand' or method == 'random':
            for ias, idxs in self.iter_block_rand(iR, R, atom):
                yield ias, idxs
        else:
            if R is None:
                R = self.maxR()

            # Create shapes
            if method == 'sphere':
                dS = (Sphere(R * (iR - 0.975)),
                      Sphere(R * (iR + 0.025)))
            elif method == 'cube':
                dS = (Cube(R * (2 * iR - 0.975)),
                      Cube(R * (2 * iR + 0.025)))

            for ias, idxs in self.iter_block_shape(dS):
                yield ias, idxs

    def copy(self):
        """ A copy of the object. """
        return self.__class__(np.copy(self.xyz),
                              atom=self.atom.copy(), sc=self.sc.copy())

    def optimize_nsc(self, axis=None, R=None):
        """ Optimize the number of supercell connections based on ``self.maxR()``

        After this routine the number of supercells may not necessarily be the same.

        This is an in-place operation.

        Parameters
        ----------
        axis : int or array_like, optional
           only optimize the specified axis (default to all)
        R : float, optional
           the maximum connection radius for each atom
        """
        if axis is None:
            axis = [0, 1, 2]
        else:
            axis = ensure_array(axis)

        if R is None:
            R = self.maxR()
        if R < 0:
            raise ValueError((self.__class__.__name__ +
                              ".optimize_nsc could not determine the radius from the "
                              "internal atoms. Provide a radius as an argument."))

        # Now we need to find the number of supercells
        nsc = np.copy(self.nsc)
        # Reset the number of supercells of the wanted optimized
        # directions to 1
        nsc[axis] = 1
        for i in axis:
            # Initialize the isc for this direction
            # (note we do not take non-orthogonal directions
            #  into account)
            isc = _a.zerosi(3)
            # Initialize the actual number of supercell connections
            # along this direction.
            prev_isc = 0
            while prev_isc == isc[i]:
                # Try next supercell connection
                isc[i] += 1
                for ia in self:
                    idx = self.close_sc(ia, isc=isc, R=R)
                    if len(idx) > 0:
                        prev_isc = isc[i]
                        break

            # Save the reached supercell connection
            nsc[i] = prev_isc * 2 + 1

        self.set_nsc(nsc)

        return nsc

    def sub(self, atom, cell=None):
        """ Create a new `Geometry` with a subset of this `Geometry`

        Indices passed *MUST* be unique.

        Negative indices are wrapped and thus works.

        Parameters
        ----------
        atom  : array_like
            indices of all atoms to be removed.
        cell   : array_like or SuperCell, optional
            the new associated cell of the geometry (defaults to the same cell)

        See Also
        --------
        SuperCell.fit : update the supercell according to a reference supercell
        remove : the negative of this routine, i.e. remove a subset of atoms
        """
        atms = self.sc2uc(atom)
        if cell is None:
            return self.__class__(self.xyz[atms, :],
                                  atom=self.atom.sub(atms), sc=self.sc.copy())
        return self.__class__(self.xyz[atms, :],
                              atom=self.atom.sub(atms), sc=cell)

    def cut(self, seps, axis, seg=0, rtol=1e-4, atol=1e-4):
        """ Returns a subset of atoms from the geometry by cutting the
        geometry into ``seps`` parts along the direction ``axis``.
        It will then _only_ return the first cut.

        This will effectively change the unit-cell in the ``axis`` as-well
        as removing ``self.na/seps`` atoms.
        It requires that ``self.na % seps == 0``.

        REMARK: You need to ensure that all atoms within the first
        cut out region are within the primary unit-cell.

        Doing ``geom.cut(2, 1).tile(2, 1)``, could for symmetric setups,
        be equivalent to a no-op operation. A ``UserWarning`` will be issued
        if this is not the case.

        Parameters
        ----------
        seps  : int
            number of times the structure will be cut.
        axis  : int
            the axis that will be cut
        seg : int, optional
            returns the i'th segment of the cut structure
            Currently the atomic coordinates are not translated,
            this may change in the future.
        rtol : (tolerance for checking tiling, see `numpy.allclose`)
        atol : (tolerance for checking tiling, see `numpy.allclose`)
        """
        if self.na % seps != 0:
            raise ValueError(
                'The system cannot be cut into {0} different '.format(seps) +
                'pieces. Please check your geometry and input.')
        # Truncate to the correct segments
        lseg = seg % seps
        # Cut down cell
        sc = self.sc.cut(seps, axis)
        # List of atoms
        n = self.na // seps
        off = n * lseg
        new = self.sub(_a.arangei(off, off + n), cell=sc)
        if not np.allclose(new.tile(seps, axis).xyz, self.xyz,
                           rtol=rtol, atol=atol):
            st = 'The cut structure cannot be re-created by tiling'
            st += '\nThe difference between the coordinates can be altered using rtol, atol'
            warnings.warn(st, UserWarning)
        return new

    def remove(self, atom):
        """ Remove atoms from the geometry.

        Indices passed *MUST* be unique.

        Negative indices are wrapped and thus works.

        Parameters
        ----------
        atom  : array_like
            indices of all atoms to be removed.

        See Also
        --------
        sub : the negative of this routine, i.e. retain a subset of atoms
        """
        atom = self.sc2uc(atom)
        atom = np.delete(_a.arangei(self.na), atom)
        return self.sub(atom)

    def tile(self, reps, axis):
        """ Tile the geometry to create a bigger one

        The atomic indices are retained for the base structure.

        Parameters
        ----------
        reps  : int
           number of tiles (repetitions)
        axis  : int
           direction of tiling, 0, 1, 2 according to the cell-direction

        Examples
        --------
        >>> geom = Geometry([[0, 0, 0], [0.5, 0, 0]], sc=1.)
        >>> g = geom.tile(2,axis=0)
        >>> print(g.xyz)
        [[ 0.   0.   0. ]
         [ 0.5  0.   0. ]
         [ 1.   0.   0. ]
         [ 1.5  0.   0. ]]
        >>> g = geom.tile(2,0).tile(2,axis=1)
        >>> print(g.xyz)
        [[ 0.   0.   0. ]
         [ 0.5  0.   0. ]
         [ 1.   0.   0. ]
         [ 1.5  0.   0. ]
         [ 0.   1.   0. ]
         [ 0.5  1.   0. ]
         [ 1.   1.   0. ]
         [ 1.5  1.   0. ]]

        See Also
        --------
        repeat : equivalent but different ordering of final structure
        """
        if reps < 1:
            raise ValueError(self.__class__.__name__ + '.tile() requires a repetition above 0')

        sc = self.sc.tile(reps, axis)

        # Our first repetition *must* be with
        # the former coordinate
        xyz = np.tile(self.xyz, (reps, 1))
        # We may use broadcasting rules instead of repeating stuff
        xyz.shape = (reps, self.na, 3)
        nr = _a.arangei(reps)
        nr.shape = (reps, 1)
        for i in range(3):
            # Correct the unit-cell offsets along `i`
            xyz[:, :, i] += nr * self.cell[axis, i]
        xyz.shape = (-1, 3)

        # Create the geometry and return it (note the smaller atoms array
        # will also expand via tiling)
        return self.__class__(xyz, atom=self.atom.tile(reps), sc=sc)

    def repeat(self, reps, axis):
        """ Create a repeated geometry

        The atomic indices are *NOT* retained for the base structure.

        The expansion of the atoms are basically performed using this
        algorithm:

        >>> ja = 0 # doctest: +SKIP
        >>> for ia in range(self.na): # doctest: +SKIP
        ...     for id,r in args: # doctest: +SKIP
        ...        for i in range(r): # doctest: +SKIP
        ...           ja = ia + cell[id,:] * i # doctest: +SKIP

        This method allows to utilise Bloch's theorem when creating
        Hamiltonian parameter sets for TBtrans.

        For geometries with a single atom this routine returns the same as
        `tile`.

        It is adviced to only use this for electrode Bloch's theorem
        purposes as `tile` is faster.

        Parameters
        ----------
        reps  : int
           number of repetitions
        axis  : int
           direction of repetition, 0, 1, 2 according to the cell-direction

        Examples
        --------
        >>> geom = Geometry([[0, 0, 0], [0.5, 0, 0]], sc=1)
        >>> g = geom.repeat(2,axis=0)
        >>> print(g.xyz)
        [[ 0.   0.   0. ]
         [ 1.   0.   0. ]
         [ 0.5  0.   0. ]
         [ 1.5  0.   0. ]]
        >>> g = geom.repeat(2,0).repeat(2,1)
        >>> print(g.xyz)
        [[ 0.   0.   0. ]
         [ 0.   1.   0. ]
         [ 1.   0.   0. ]
         [ 1.   1.   0. ]
         [ 0.5  0.   0. ]
         [ 0.5  1.   0. ]
         [ 1.5  0.   0. ]
         [ 1.5  1.   0. ]]

        See Also
        --------
        tile : equivalent but different ordering of final structure
        """
        if reps < 1:
            raise ValueError(self.__class__.__name__ + '.repeat() requires a repetition above 0')

        sc = self.sc.repeat(reps, axis)

        # Our first repetition *must* be with
        # the former coordinate
        xyz = np.repeat(self.xyz, reps, axis=0)
        # We may use broadcasting rules instead of repeating stuff
        xyz.shape = (self.na, reps, 3)
        nr = _a.arangei(reps)
        nr.shape = (1, reps)
        for i in range(3):
            # Correct the unit-cell offsets along `i`
            xyz[:, :, i] += nr * self.cell[axis, i]
        xyz.shape = (-1, 3)

        # Create the geometry and return it
        return self.__class__(xyz, atom=self.atom.repeat(reps), sc=sc)

    def __mul__(self, m):
        """ Implement easy repeat function

        Parameters
        ----------
        m : int or tuple or list or (tuple, str) or (list, str)
           a tuple/list may be of length 2 or 3. A length of 2 corresponds
           to tuple[0] == *number of multiplications*, tuple[1] is the
           axis.
           A length of 3 corresponds to each of the directions.
           An optional string may be used to specify the `tile` or `repeat` function.
           The default is the `tile` function.

        Examples
        --------
        >>> geometry = Geometry([0.] * 3, sc=[1.5, 3, 4])
        >>> geometry * 2 == geometry.tile(2, 0).tile(2, 1).tile(2, 2)
        True
        >>> geometry * [2, 1, 2] == geometry.tile(2, 0).tile(2, 2)
        True
        >>> geometry * [2, 2] == geometry.tile(2, 2)
        True
        >>> geometry * ([2, 1, 2], 'repeat') == geometry.repeat(2, 0).repeat(2, 2)
        True
        >>> geometry * ([2, 1, 2], 'r') == geometry.repeat(2, 0).repeat(2, 2)
        True
        >>> geometry * ([2, 0], 'r') == geometry.repeat(2, 0)
        True
        >>> geometry * ([2, 2], 'r') == geometry.repeat(2, 2)
        True

        See Also
        --------
        tile : specific method to enlarge the geometry
        repeat : specific method to enlarge the geometry
        """

        # Reverse arguments in case it is on the LHS
        if not isinstance(self, Geometry):
            return m * self

        # Simple form
        if isinstance(m, Integral):
            return self * [m, m, m]

        # Error in argument, fall-back
        if len(m) == 1:
            return self * m[0]

        # Look-up table
        method_tbl = {'r': 'repeat',
                  'repeat': 'repeat',
                  't': 'tile',
                  'tile': 'tile'}
        method = 'tile'

        # Determine the type
        if len(m) == 2:
            # either
            #  (r, axis)
            #  ((...), method
            if isinstance(m[1], _str):
                method = method_tbl[m[1]]
                m = m[0]

        if len(m) == 1:
            #  r
            m = m[0]
            g = self.copy()
            for i in range(3):
                g = getattr(g, method)(m, i)

        elif len(m) == 2:
            #  (r, axis)
            g = getattr(self, method)(m[0], m[1])

        elif len(m) == 3:
            #  (r, r, r)
            g = self.copy()
            for i in range(3):
                g = getattr(g, method)(m[i], i)

        else:
            raise ValueError('Multiplying a geometry has received a wrong argument')

        return g

    __rmul__ = __mul__

    def angle(self, atom, dir=(1., 0, 0), ref=None, rad=False):
        r""" The angle between atom `atom` and the direction `dir`, with possibility of a reference coordinate `ref`

        The calculated angle can be written as this

        .. math::
            \alpha = \arccos \frac{(\mathrm{atom} - \mathrm{ref})\cdot \mathrm{dir}}
            {|\mathrm{atom}-\mathrm{ref}||\mathrm{dir}|}

        and thus lies in the interval :math:`[0 ; \pi]` as one cannot distinguish orientation without
        additional vectors.

        Parameters
        ----------
        atom : int or array_like
           atomic index
        dir : str, int or vector
           the direction from which the angle is calculated from, default to ``x``
        ref : int or coordinate, optional
           the reference point from which the vectors are drawn, default to origo
        rad : bool, optional
           whether the returned value is in radians
        """
        xi = self.axyz(ensure_array(atom))
        if isinstance(dir, (_str, Integral)):
            dir = self.cell[direction(dir), :]
        else:
            dir = ensure_array(dir, np.float64)
        # Normalize so we don't have to have this in the
        # below formula
        dir /= (dir ** 2).sum() ** .5
        # Broad-casting
        dir.shape = (1, -1)

        if ref is None:
            pass
        elif isinstance(ref, Integral):
            xi -= self.axyz(ref)[None, :]
        else:
            xi -= ensure_array(ref, np.float64)[None, :]
        nx = (xi ** 2).sum(axis=1) ** .5
        ang = np.where(nx > 1e-6, np.arccos((xi * dir).sum(axis=1) / nx), 0.)
        if rad:
            return ang
        return np.degrees(ang)

    def rotatea(self, angle, origo=None, atom=None, only='abc+xyz', rad=False):
        """ Rotate around first lattice vector

        See Also
        --------
        rotate : generic function of this, this routine calls `rotate` with `v = self.cell[0, :]`
        """
        return self.rotate(angle, self.cell[0, :], origo, atom, only, rad)

    def rotateb(self, angle, origo=None, atom=None, only='abc+xyz', rad=False):
        """ Rotate around second lattice vector

        See Also
        --------
        rotate : generic function of this, this routine calls `rotate` with `v = self.cell[1, :]`
        """
        return self.rotate(angle, self.cell[1, :], origo, atom, only, rad)

    def rotatec(self, angle, origo=None, atom=None, only='abc+xyz', rad=False):
        """ Rotate around third lattice vector

        See Also
        --------
        rotate : generic function of this, this routine calls `rotate` with `v = self.cell[2, :]`
        """
        return self.rotate(angle, self.cell[2, :], origo, atom, only, rad)

    def rotate(self, angle, v, origo=None, atom=None, only='abc+xyz', rad=False):
        """ Rotate geometry around vector and return a new geometry

        Per default will the entire geometry be rotated, such that everything
        is aligned as before rotation.

        However, by supplying ``only = 'abc|xyz'`` one can designate which
        part of the geometry that will be rotated.

        Parameters
        ----------
        angle : float
             the angle in radians of which the geometry should be rotated
        v     : array_like
             the normal vector to the rotated plane, i.e.
             v = [1,0,0] will rotate the ``yz`` plane
        origo : int or array_like, optional
             the origin of rotation. Anything but [0, 0, 0] is equivalent
             to a `self.move(-origo).rotate(...).move(origo)`.
             If this is an `int` it corresponds to the atomic index.
        atom : int or array_like, optional
             only rotate the given atomic indices, if not specified, all
             atoms will be rotated.
        only  : {'abc+xyz', 'xyz', 'abc'}
             which coordinate subject should be rotated,
             if ``abc`` is in this string the cell will be rotated
             if ``xyz`` is in this string the coordinates will be rotated

        See Also
        --------
        Quaternion : class to rotate
        rotatea : generic function for rotating around first lattice vector
        rotateb : generic function for rotating around second lattice vector
        rotatec : generic function for rotating around third lattice vector
        """
        if origo is None:
            origo = [0., 0., 0.]
        elif isinstance(origo, Integral):
            origo = self.axyz(origo)
        origo = ensure_array(origo, np.float64)

        if not atom is None:
            # Only rotate the unique values
            atom = self.sc2uc(atom, uniq=True)

        # Ensure the normal vector is normalized...
        vn = np.copy(_a.asarrayd(v))
        vn /= (vn ** 2).sum() ** .5

        # Prepare quaternion...
        q = Quaternion(angle, vn, rad=rad)
        q /= q.norm()

        # Rotate by direct call
        if 'abc' in only:
            sc = self.sc.rotate(angle, vn, rad=rad, only=only)
        else:
            sc = self.sc.copy()

        # Copy
        xyz = np.copy(self.xyz)

        if 'xyz' in only:
            # subtract and add origo, before and after rotation
            xyz[atom, :] = q.rotate(xyz[atom, :] - origo[None, :]) + origo[None, :]

        return self.__class__(xyz, atom=self.atom.copy(), sc=sc)

    def rotate_miller(self, m, v):
        """ Align Miller direction along ``v``

        Rotate geometry and cell such that the Miller direction
        points along the Cartesian vector ``v``.
        """
        # Create normal vector to miller direction and cartesian
        # direction
        cp = _a.arrayd([m[1] * v[2] - m[2] * v[1],
                        m[2] * v[0] - m[0] * v[2],
                        m[0] * v[1] - m[1] * v[0]])
        cp /= (cp ** 2).sum() ** .5

        lm = _a.arrayd(m)
        lm /= (lm ** 2).sum() ** .5
        lv = _a.arrayd(v)
        lv /= (lv ** 2).sum() ** .5

        # Now rotate the angle between them
        a = acos(np.sum(lm * lv))
        return self.rotate(a, cp)

    def move(self, v, atom=None, cell=False):
        """ Translates the geometry by ``v``

        One can translate a subset of the atoms by supplying ``atom``.

        Returns a copy of the structure translated by ``v``.

        Parameters
        ----------
        v     : array_like
             the vector to displace all atomic coordinates
        atom : int or array_like, optional
             only displace the given atomic indices, if not specified, all
             atoms will be displaced
        cell  : bool, optional
             If True the supercell also gets enlarged by the vector
        """
        g = self.copy()
        if atom is None:
            g.xyz[:, :] += np.asarray(v, g.xyz.dtype)[None, :]
        else:
            g.xyz[ensure_array(atom), :] += np.asarray(v, g.xyz.dtype)[None, :]
        if cell:
            g.set_supercell(g.sc.translate(v))
        return g
    translate = move

    def swap(self, a, b):
        """ Swap a set of atoms in the geometry and return a new one

        This can be used to reorder elements of a geometry.

        Parameters
        ----------
        a : array_like
             the first list of atomic coordinates
        b : array_like
             the second list of atomic coordinates
        """
        a = ensure_array(a)
        b = ensure_array(b)
        xyz = np.copy(self.xyz)
        xyz[a, :] = self.xyz[b, :]
        xyz[b, :] = self.xyz[a, :]
        return self.__class__(xyz, atom=self.atom.swap(a, b), sc=self.sc.copy())

    def swapaxes(self, a, b, swap='cell+xyz'):
        """ Swap the axis for the atomic coordinates and the cell vectors

        If ``swapaxes(0,1)`` it returns the 0 and 1 values
        swapped in the ``cell`` variable.

        Parameters
        ----------
        a : int
           axes 1, swaps with ``b``
        b : int
           axes 2, swaps with ``a``
        swap : {'cell+xyz', 'cell', 'xyz'}
           decide what to swap, if `'cell'` is in `swap` then
           the cell axis are swapped.
           if `'xyz'` is in `swap` then
           the xyz (Cartesian) axis are swapped.
           Both may be in `swap`.
        """
        xyz = np.copy(self.xyz)
        if 'xyz' in swap:
            xyz[:, a] = self.xyz[:, b]
            xyz[:, b] = self.xyz[:, a]
        if 'cell' in swap:
            sc = self.sc.swapaxes(a, b)
        else:
            sc = self.sc.copy()
        return self.__class__(xyz, atom=self.atom.copy(), sc=sc)

    def center(self, atom=None, what='xyz'):
        """ Returns the center of the geometry

        By specifying `what` one can control whether it should be:

        * ``xyz|position``: Center of coordinates (default)
        * ``mass``: Center of mass
        * ``cell``: Center of cell

        Parameters
        ----------
        atom : array_like
            list of atomic indices to find center of
        what : {'xyz', 'mass', 'cell'}
            determine whether center should be of 'cell', mass-centered ('mass'),
            or absolute center of the positions.
        """
        if 'cell' in what:
            return self.sc.center()
        if atom is None:
            g = self
        else:
            g = self.sub(ensure_array(atom))
        if 'mass' in what:
            mass = self.mass
            return np.dot(mass, g.xyz) / np.sum(mass)
        if not ('xyz' in what or 'position' in what):
            raise ValueError(
                'Unknown what, not one of [xyz,position,mass,cell]')
        return np.mean(g.xyz, axis=0)

    def append(self, other, axis):
        """ Appends structure along ``axis``. This will automatically
        add the ``self.cell[axis,:]`` to all atomic coordiates in the
        ``other`` structure before appending.

        The basic algorithm is this:

        >>> oxa = other.xyz + self.cell[axis,:][None,:] # doctest: +SKIP
        >>> self.xyz = np.append(self.xyz,oxa) # doctest: +SKIP
        >>> self.cell[axis,:] += other.cell[axis,:] # doctest: +SKIP

        NOTE: The cell appended is only in the axis that
        is appended, which means that the other cell directions
        need not conform.

        Parameters
        ----------
        other : Geometry or SuperCell
            Other geometry class which needs to be appended
            If a ``SuperCell`` only the super cell will be extended
        axis  : int
            Cell direction to which the ``other`` geometry should be
            appended.

        See Also
        --------
        add : add geometries
        prepend : prending geometries
        attach : attach a geometry
        insert : insert a geometry
        """
        if isinstance(other, SuperCell):
            # Only extend the supercell.
            xyz = np.copy(self.xyz)
            atom = self.atom.copy()
            sc = self.sc.append(other, axis)
        else:
            xyz = np.append(self.xyz,
                            self.cell[axis, :][None, :] + other.xyz,
                            axis=0)
            atom = self.atom.append(other.atom)
            sc = self.sc.append(other.sc, axis)
        return self.__class__(xyz, atom=atom, sc=sc)

    def prepend(self, other, axis):
        """
        Prepends structure along ``axis``. This will automatically
        add the ``self.cell[axis,:]`` to all atomic coordiates in the
        ``other`` structure before prepending.

        The basic algorithm is this:

        >>> oxa = other.xyz # doctest: +SKIP
        >>> self.xyz = np.append(oxa, self.xyz + other.cell[axis,:][None,:]) # doctest: +SKIP
        >>> self.cell[axis,:] += other.cell[axis,:] # doctest: +SKIP

        NOTE: The cell prepended is only in the axis that
        is prependend, which means that the other cell directions
        need not conform.

        Parameters
        ----------
        other : Geometry or SuperCell
            Other geometry class which needs to be prepended
            If a ``SuperCell`` only the super cell will be extended
        axis  : int
            Cell direction to which the ``other`` geometry should be
            prepended

        See Also
        --------
        add : add geometries
        append : appending geometries
        attach : attach a geometry
        insert : insert a geometry
        """
        if isinstance(other, SuperCell):
            # Only extend the supercell.
            xyz = np.copy(self.xyz)
            atom = self.atom.copy()
            sc = self.sc.prepend(other, axis)
        else:
            xyz = np.append(other.xyz,
                            self.xyz + other.cell[axis, :][None, :],
                            axis=0)
            atom = self.atom.prepend(other.atom)
            sc = self.sc.append(other.sc, axis)
        return self.__class__(xyz, atom=atom, sc=sc)

    def add(self, other):
        """
        Adds atoms (as is) from the ``other`` geometry.
        This will not alter the cell vectors.

        Parameters
        ----------
        other : Geometry
            Other geometry class which is added

        See Also
        --------
        append : appending geometries
        prepend : prending geometries
        attach : attach a geometry
        insert : insert a geometry
        """
        xyz = np.append(self.xyz, other.xyz, axis=0)
        sc = self.sc.copy()
        return self.__class__(xyz, atom=self.atom.add(other.atom), sc=sc)

    def insert(self, atom, geom):
        """ Inserts other atoms right before index

        We insert the ``geom`` `Geometry` before `atom`.
        Note that this will not change the unit cell.

        Parameters
        ----------
        atom : int
           the index at which atom the other geometry is inserted
        geom : Geometry
           the other geometry to be inserted

        See Also
        --------
        add : add geometries
        append : appending geometries
        prepend : prending geometries
        attach : attach a geometry
        """
        xyz = np.insert(self.xyz, atom, geom.xyz, axis=0)
        atoms = self.atom.insert(atom, geom.atom)
        return self.__class__(xyz, atom=atoms, sc=self.sc.copy())

    def __add__(a, b):
        """ Merge two geometries

        Parameters
        ----------
        a, b : Geometry or tuple or list
           when adding a Geometry with a Geometry it defaults to using `add` function
           with the LHS retaining the cell-vectors.
           a tuple/list may be of length 2 with the first element being a Geometry and the second
           being an integer specifying the lattice vector where it is appended.
           One may also use a `SuperCell` instead of a `Geometry` which behaves similarly.

        Examples
        --------

        >>> A + B == A.add(B) # doctest: +SKIP
        >>> A + (B, 1) == A.append(B, 1) # doctest: +SKIP
        >>> A + (B, 2) == A.append(B, 2) # doctest: +SKIP
        >>> (A, 1) + B == A.prepend(B, 1) # doctest: +SKIP

        See Also
        --------
        add : add geometries
        append : appending geometries
        prepend : prending geometries
        """

        if isinstance(a, Geometry):
            if isinstance(b, Geometry):
                return a.add(b)
            return a.append(b[0], b[1])
        elif isinstance(b, Geometry):
            return a.prepend(b[0], b[1])

        raise ValueError('Arguments for adding (add/append/prepend) are incorrect')

    __radd__ = __add__

    def attach(self, s_idx, other, o_idx, dist='calc', axis=None):
        """ Attaches another ``Geometry`` at the `s_idx` index with respect to `o_idx` using different methods.

        Parameters
        ----------
        dist : ``array_like``, ``float``, ``str`` (`'calc'`)
           the distance (in `Ang`) between the attached coordinates.
           If `dist` is `arraylike it should be the vector between
           the atoms;
           if `dist` is `float` the argument `axis` is required
           and the vector will be calculated along the corresponding latticevector;
           else if `dist` is `str` this will correspond to the
           `method` argument of the ``Atom.radius`` class of the two
           atoms. Here `axis` is also required.
        axis : ``int``
           specify the direction of the lattice vectors used.
           Not used if `dist` is an array-like argument.
        """
        if isinstance(dist, Real):
            # We have a single rational number
            if axis is None:
                raise ValueError("Argument `axis` has not been specified, please specify the axis when using a distance")

            # Now calculate the vector that we should have
            # between the atoms
            v = self.cell[axis, :]
            v = v / (v[0]**2 + v[1]**2 + v[2]**2) ** .5 * dist

        elif isinstance(dist, string_types):
            # We have a single rational number
            if axis is None:
                raise ValueError("Argument `axis` has not been specified, please specify the axis when using a distance")

            # This is the empirical distance between the atoms
            d = self.atom[s_idx].radius(dist) + other.atom[o_idx].radius(dist)
            if isinstance(axis, Integral):
                v = self.cell[axis, :]
            else:
                v = np.array(axis)

            v = v / (v[0]**2 + v[1]**2 + v[2]**2) ** .5 * d

        else:
            # The user *must* have supplied a vector
            v = np.array(dist)

        # Now create a copy of the other geometry
        # so that we move it...
        # Translate to origo, then back to position in new cell
        o = other.translate(-other.xyz[o_idx] + self.xyz[s_idx] + v)

        # We do not know how to handle the lattice-vectors,
        # so we will do nothing...
        return self.add(o)

    def reverse(self, atom=None):
        """ Returns a reversed geometry

        Also enables reversing a subset of the atoms.

        Parameters
        ----------
        atom : int or array_like, optional
             only reverse the given atomic indices, if not specified, all
             atoms will be reversed
        """
        if atom is None:
            xyz = self.xyz[::-1, :]
        else:
            atom = ensure_array(atom)
            xyz = np.copy(self.xyz)
            xyz[atom, :] = self.xyz[atom[::-1], :]
        return self.__class__(xyz, atom=self.atom.reverse(atom), sc=self.sc.copy())

    def mirror(self, plane, atom=None):
        """ Mirrors the structure around the center of the atoms """
        if not atom is None:
            atom = ensure_array(atom)
        else:
            atom = slice(None)
        g = self.copy()
        lplane = ''.join(sorted(plane.lower()))
        if lplane == 'xy':
            g.xyz[atom, 2] *= -1
        elif lplane == 'yz':
            g.xyz[atom, 0] *= -1
        elif lplane == 'xz':
            g.xyz[atom, 1] *= -1
        return self.__class__(g.xyz, atom=g.atom, sc=self.sc.copy())

    @property
    def fxyz(self):
        """ Returns geometry coordinates in fractional coordinates """
        return lin.solve(self.cell.T, self.xyz.T).T

    def axyz(self, atom=None, isc=None):
        """ Return the atomic coordinates in the supercell of a given atom.

        The `Geometry[...]` slicing is calling this function with appropriate options.

        Parameters
        ----------
        atom : int or array_like
          atom(s) from which we should return the coordinates, the atomic indices
          may be in supercell format.
        isc   : array_like, optional
            Returns the atomic coordinates shifted according to the integer
            parts of the cell. Defaults to the unit-cell

        Examples
        --------
        >>> geom = Geometry([[0, 0, 0], [0.5, 0, 0]], sc=1.)
        >>> print(geom.axyz(isc=[1,0,0]))
        [[ 1.   0.   0. ]
         [ 1.5  0.   0. ]]

        >>> geom = Geometry([[0, 0, 0], [0.5, 0, 0]], sc=1.)
        >>> print(geom.axyz(0))
        [ 0.  0.  0.]

        """
        if atom is None and isc is None:
            return self.xyz

        # If only atom has been specified
        if isc is None:
            # get offsets from atomic indices (note that this will be per atom)
            isc = self.a2isc(atom)
            offset = self.sc.offset(isc)
            return self.xyz[self.sc2uc(atom), :] + offset

        elif atom is None:
            offset = self.sc.offset(isc)
            return self.xyz[:, :] + offset[None, :]

        # Neither of atom, or isc are `None`, we add the offset to all coordinates
        offset = self.sc.offset(isc)
        if isinstance(atom, Integral):
            return self.axyz(atom) + offset

        return self.axyz(atom) + offset[None, :]

    def scale(self, scale):
        """ Scale coordinates and unit-cell to get a new geometry with proper scaling

        Parameters
        ----------
        scale : float
           the scale factor for the new geometry (lattice vectors, coordinates
           and the atomic radii are scaled).
        """
        xyz = self.xyz * scale
        atom = self.atom.scale(scale)
        sc = self.sc.scale(scale)
        return self.__class__(xyz, atom=atom, sc=sc)

    def within_sc(self, shapes, isc=None,
                  idx=None, idx_xyz=None,
                  ret_xyz=False, ret_rij=False):
        """ Indices of atoms in a given supercell within a given shape from a given coordinate

        This returns a set of atomic indices which are within a
        sphere of radius ``R``.

        If R is a tuple/list/array it will return the indices:
        in the ranges:

        >>> ( x <= R[0] , R[0] < x <= R[1], R[1] < x <= R[2] ) # doctest: +SKIP

        Parameters
        ----------
        shapes  : Shape or list of Shape
            A list of increasing shapes that define the extend of the geometric
            volume that is searched.
            It is vital that::

               shapes[0] in shapes[1] in shapes[2] ...
        isc       : array_like, optional
            The super-cell which the coordinates are checked in. Defaults to `[0, 0, 0]`
        idx       : array_like, optional
            List of atoms that will be considered. This can
            be used to only take out a certain atoms.
        idx_xyz : array_like, optional
            The atomic coordinates of the equivalent ``idx`` variable (``idx`` must also be passed)
        ret_xyz : bool, optional
            If True this method will return the coordinates
            for each of the couplings.
        ret_rij : bool, optional
            If True this method will return the distance
            for each of the couplings.
        """

        # Ensure that `shapes` is a list
        if isinstance(shapes, Shape):
            shapes = [shapes]
        nshapes = len(shapes)

        # Convert to actual array
        if idx is not None:
            if not isndarray(idx):
                idx = ensure_array(idx)
        else:
            # If idx is None, then idx_xyz cannot be used!
            # So we force it to None
            idx_xyz = None

        # Get shape centers
        off = shapes[-1].center[:]
        # Get the supercell offset
        soff = self.sc.offset(isc)[:]

        # Get atomic coordinate in principal cell
        if idx_xyz is None:
            xa = self[idx, :] + soff[None, :]
        else:
            # For extremely large systems re-using the
            # idx_xyz is faster than indexing
            # a very large array
            # However, this idx_xyz should not
            # be offset by any supercell
            xa = idx_xyz[:, :] + soff[None, :]

        # Get indices and coordinates of the largest shape
        # The largest part of the calculation are to calculate
        # the content in the largest shape.
        ix = shapes[-1].iwithin(xa)
        # Reduce search space
        xa = xa[ix, :]

        if idx is None:
            # This is because of the pre-check of the distance checks
            idx = ix
        else:
            idx = idx[ix]

        if len(xa) == 0:
            # Quick return if there are no entries...

            ret = [[np.empty([0], np.int32)] * nshapes]
            rc = 0
            if ret_xyz:
                rc = rc + 1
                ret.append([np.empty([0, 3], np.float64)] * nshapes)
            if ret_rij:
                rd = rc + 1
                ret.append([np.empty([0], np.float64)] * nshapes)

            if nshapes == 1:
                if ret_xyz and ret_rij:
                    return [ret[0][0], ret[1][0], ret[2][0]]
                elif ret_xyz or ret_rij:
                    return [ret[0][0], ret[1][0]]
                return ret[0][0]
            if ret_xyz or ret_rij:
                return ret
            return ret[0]

        # Calculate distance
        if ret_rij:
            d = np.sum((xa - off[None, :]) ** 2, axis=1) ** .5

        # Create the initial lists that we will build up
        # Then finally, we will return the reversed lists

        # Quick return
        if nshapes == 1:
            ret = [[idx]]
            if ret_xyz:
                ret.append([xa])
            if ret_rij:
                ret.append([d])
            if ret_xyz or ret_rij:
                return ret
            return ret[0]

        # TODO Check that all shapes coincide with the following shapes

        # Now we create a list of indices which coincide
        # in each of the shapes
        # Do a reduction on each of the list elements
        ixS = []
        cum = np.array([], idx.dtype)
        for i, s in enumerate(shapes):
            x = s.iwithin(xa)
            if i > 0:
                x = np.setdiff1d(x, cum, assume_unique=True)
            # Update elements to remove in next loop
            cum = np.append(cum, x)
            ixS.append(x)

        # Do for the first shape
        ret = [[ensure_array(idx[ixS[0]])]]
        rc = 0
        if ret_xyz:
            rc = rc + 1
            ret.append([xa[ixS[0], :]])
        if ret_rij:
            rd = rc + 1
            ret.append([d[ixS[0]]])
        for i in range(1, nshapes):
            ret[0].append(ensure_array(idx[ixS[i]]))
            if ret_xyz:
                ret[rc].append(xa[ixS[i], :])
            if ret_rij:
                ret[rd].append(d[ixS[i]])

        if ret_xyz or ret_rij:
            return ret
        return ret[0]

    def close_sc(self, xyz_ia, isc=(0, 0, 0), R=None,
                 idx=None, idx_xyz=None,
                 ret_xyz=False, ret_rij=False):
        """ Indices of atoms in a given supercell within a given radius from a given coordinate

        This returns a set of atomic indices which are within a
        sphere of radius `R`.

        If `R` is a tuple/list/array it will return the indices:
        in the ranges:

        >>> ( x <= R[0] , R[0] < x <= R[1], R[1] < x <= R[2] ) # doctest: +SKIP

        Parameters
        ----------
        xyz_ia : array_like of floats or int
            Either a point in space or an index of an atom.
            If an index is passed it is the equivalent of passing
            the atomic coordinate ``close_sc(self.xyz[xyz_ia,:])``.
        isc : array_like, optional
            The super-cell which the coordinates are checked in.
        R : float or array_like, optional
            The radii parameter to where the atomic connections are found.
            If `R` is an array it will return the indices:
            in the ranges ``( x <= R[0] , R[0] < x <= R[1], R[1] < x <= R[2] )``.
            If a single float it will return ``x <= R``.
        idx : array_like of int, optional
            List of atoms that will be considered. This can
            be used to only take out a certain atoms.
        idx_xyz : array_like of float, optional
            The atomic coordinates of the equivalent `idx` variable (`idx` must also be passed)
        ret_xyz : bool, optional
            If True this method will return the coordinates
            for each of the couplings.
        ret_rij : bool, optional
            If True this method will return the distance
            for each of the couplings.
        """

        # Common numpy used functions (reduces function look-ups)
        log_and = np.logical_and
        fabs = np.fabs

        if R is None:
            R = np.array([self.maxR()], np.float64)
        elif not isndarray(R):
            R = ensure_array(R, np.float64)

        # Maximum distance queried
        max_R = R[-1]

        # Convert to actual array
        if idx is not None:
            if not isndarray(idx):
                idx = ensure_array(idx)
        else:
            # If idx is None, then idx_xyz cannot be used!
            idx_xyz = None

        if isinstance(xyz_ia, Integral):
            off = self.xyz[xyz_ia, :]
        elif not isndarray(xyz_ia):
            off = ensure_array(xyz_ia, np.float64)
        else:
            off = xyz_ia

        # Calculate the complete offset
        foff = self.sc.offset(isc)[:] - off[:]

        # Get atomic coordinate in principal cell
        if idx_xyz is None:
            dxa = self[idx, :] + foff[None, :]
        else:
            # For extremely large systems re-using the
            # idx_xyz is faster than indexing
            # a very large array
            dxa = idx_xyz[:, :] + foff[None, :]

        # Immediately downscale by easy checking
        # This will reduce the computation of the vector-norm
        # which is the main culprit of the time-consumption
        # This abstraction will _only_ help very large
        # systems.
        # For smaller ones this will actually be a slower
        # method...
        if dxa.shape[0] > 10000:
            if idx is None:
                # first
                ix = fabs(dxa[:, 0]) <= max_R
                idx = ix.nonzero()[0]
                dxa = dxa[ix, :]
                # second
                ix = fabs(dxa[:, 1]) <= max_R
                idx = idx[ix]
                dxa = dxa[ix, :]
                # third
                ix = fabs(dxa[:, 2]) <= max_R
                idx = idx[ix]
                dxa = dxa[ix, :]
            else:
                for i in [0, 1, 2]:
                    ix = fabs(dxa[:, i]) <= max_R
                    idx = idx[ix]
                    dxa = dxa[ix, :]
        else:
            ix = log_and.reduce(fabs(dxa[:, :]) <= max_R, axis=1)

            if idx is None:
                # This is because of the pre-check of the
                # distance checks
                idx = ix.nonzero()[0]
            else:
                idx = idx[ix]
            dxa = dxa[ix, :]

        # Create default return
        ret = [[np.empty([0], np.int32)] * len(R)]
        i = 0
        if ret_xyz:
            i += 1
            rc = i
            ret.append([np.empty([0, 3], np.float64)] * len(R))
        if ret_rij:
            i += 1
            rc = i
            ret.append([np.empty([0], np.float64)] * len(R))

        if len(dxa) == 0:
            # Quick return if there are
            # no entries...
            if len(R) == 1:
                if ret_xyz and ret_rij:
                    return [ret[0][0], ret[1][0], ret[2][0]]
                elif ret_xyz or ret_rij:
                    return [ret[0][0], ret[1][0]]
                return ret[0][0]
            if ret_xyz or ret_rij:
                return ret
            return ret[0]

        # Retrieve all atomic indices which are closer
        # than our delta-R
        # The linear algebra norm function could be used, but it
        # has a lot of checks, hence we do it manually
        # xaR = np.linalg.norm(dxa,axis=-1)

        # It is faster to do a single multiplacation than
        # a sqrt of MANY values
        # After having reduced the dxa array, we may then
        # take the sqrt
        max_R = max_R * max_R
        xaR = dxa[:, 0]**2 + dxa[:, 1]**2 + dxa[:, 2]**2
        ix = (xaR <= max_R).nonzero()[0]

        # Reduce search space and correct distances
        d = xaR[ix] ** .5
        if ret_xyz:
            xa = dxa[ix, :] + off[None, :]
        del xaR, dxa  # just because these arrays could be very big...

        # Check whether we only have one range to check.
        # If so, we need not reduce the index space
        if len(R) == 1:
            ret = [idx[ix]]
            if ret_xyz:
                ret.append(xa)
            if ret_rij:
                ret.append(d)
            if ret_xyz or ret_rij:
                return ret
            return ret[0]

        if np.any(np.diff(R) < 0.):
            raise ValueError(('Proximity checks for several quantities '
                              'at a time requires ascending R values.'))

        # The more neigbours you wish to find the faster this becomes
        # We only do "one" heavy duty search,
        # then we immediately reduce search space to this subspace
        tidx = (d <= R[0]).nonzero()[0]
        ret = [[ensure_array(idx[ix[tidx]])]]
        i = 0
        if ret_xyz:
            rc = i + 1
            i += 1
            ret.append([xa[tidx]])
        if ret_rij:
            rd = i + 1
            i += 1
            ret.append([d[tidx]])
        for i in range(1, len(R)):
            # Search in the sub-space
            # Notice that this sub-space reduction will never
            # allow the same indice to be in two ranges (due to
            # numerics)
            tidx = log_and(R[i - 1] < d, d <= R[i]).nonzero()[0]
            ret[0].append(ensure_array(idx[ix[tidx]]))
            if ret_xyz:
                ret[rc].append(xa[tidx])
            if ret_rij:
                ret[rd].append(d[tidx])

        if ret_xyz or ret_rij:
            return ret
        return ret[0]

    def bond_correct(self, ia, atom, method='calc'):
        """ Corrects the bond between `ia` and the `atom`.

        Corrects the bond-length between atom `ia` and `atom` in such
        a way that the atomic radius is preserved.
        I.e. the sum of the bond-lengths minimizes the distance matrix.

        Only atom `ia` is moved.

        Parameters
        ----------
        ia : int
            The atom to be displaced according to the atomic radius
        atom : array_like or int
            The atom(s) from which the radius should be reduced.
        method : ``str``, ``float``
            If str will use that as lookup in `Atom.radius`.
            Else it will be the new bond-length.
        """

        # Decide which algorithm to choose from
        if isinstance(atom, Integral):
            # a single point
            algo = atom
        elif len(atom) == 1:
            algo = atom[0]
        else:
            # signal a list of atoms
            algo = -1

        if algo >= 0:

            # We have a single atom
            # Get bond length in the closest direction
            # A bond-length HAS to be below 10
            idx, c, d = self.close(ia, R=(0.1, 10.), idx=algo,
                                   ret_xyz=True, ret_rij=True)
            i = np.argmin(d[1])
            # Convert to unitcell atom (and get the one atom)
            idx = self.sc2uc(idx[1][i])
            c = c[1][i]
            d = d[1][i]

            # Calculate the bond vector
            bv = self.xyz[ia, :] - c

            try:
                # If it is a number, we use that.
                rad = float(method)
            except Exception:
                # get radius
                rad = self.atom[idx].radius(method) \
                      + self.atom[ia].radius(method)

            # Update the coordinate
            self.xyz[ia, :] = c + bv / d * rad

        else:
            raise NotImplementedError(
                'Changing bond-length dependent on several lacks implementation.')

    def within(self, shapes,
            idx=None, idx_xyz=None,
            ret_xyz=False, ret_rij=False):
        """ Indices of atoms in the entire supercell within a given shape from a given coordinate

        This heavily relies on the `within_sc` method.

        Note that if a connection is made in a neighbouring super-cell
        then the atomic index is shifted by the super-cell index times
        number of atoms.
        This allows one to decipher super-cell atoms from unit-cell atoms.

        Parameters
        ----------
        shapes : Shape, list of Shape
        idx     : array_like, optional
            List of indices for atoms that are to be considered
        idx_xyz : array_like, optional
            The atomic coordinates of the equivalent ``idx`` variable (``idx`` must also be passed)
        ret_xyz : bool, optional
            If true this method will return the coordinates
            for each of the couplings.
        ret_rij : bool, optional
            If true this method will return the distances from the ``xyz_ia``
            for each of the couplings.
        """

        # Ensure that `shapes` is a list
        if isinstance(shapes, Shape):
            shapes = [shapes]
        nshapes = len(shapes)

        # Get global calls
        # Is faster for many loops
        concat = np.concatenate

        ret = [[np.empty([0], np.int32)] * nshapes]
        i = 0
        if ret_xyz:
            c = i + 1
            i += 1
            ret.append([np.empty([0, 3], np.float64)] * nshapes)
        if ret_rij:
            d = i + 1
            i += 1
            ret.append([np.empty([0], np.float64)] * nshapes)

        ret_special = ret_xyz or ret_rij

        for s in range(self.n_s):
            na = self.na * s
            sret = self.within_sc(shapes, self.sc.sc_off[s, :],
                                  idx=idx, idx_xyz=idx_xyz,
                                  ret_xyz=ret_xyz, ret_rij=ret_rij)
            if not ret_special:
                # This is to "fake" the return
                # of a list (we will do indexing!)
                sret = [sret]

            if isinstance(sret[0], list):
                # we have a list of arrays (nshapes > 1)
                for i, x in enumerate(sret[0]):
                    ret[0][i] = concat((ret[0][i], x + na), axis=0)
                    if ret_xyz:
                        ret[c][i] = concat((ret[c][i], sret[c][i]), axis=0)
                    if ret_rij:
                        ret[d][i] = concat((ret[d][i], sret[d][i]), axis=0)
            elif len(sret[0]) > 0:
                # We can add it to the list (nshapes == 1)
                # We add the atomic offset for the supercell index
                ret[0][0] = concat((ret[0][0], sret[0] + na), axis=0)
                if ret_xyz:
                    ret[c][0] = concat((ret[c][0], sret[c]), axis=0)
                if ret_rij:
                    ret[d][0] = concat((ret[d][0], sret[d]), axis=0)

        if nshapes == 1:
            if ret_xyz and ret_rij:
                return [ret[0][0], ret[1][0], ret[2][0]]
            elif ret_xyz or ret_rij:
                return [ret[0][0], ret[1][0]]
            return ret[0][0]

        if ret_special:
            return ret

        return ret[0]

    def close(self, xyz_ia, R=None,
            idx=None, idx_xyz=None,
            ret_xyz=False, ret_rij=False):
        """ Indices of atoms in the entire supercell within a given radius from a given coordinate

        This heavily relies on the `close_sc` method.

        Note that if a connection is made in a neighbouring super-cell
        then the atomic index is shifted by the super-cell index times
        number of atoms.
        This allows one to decipher super-cell atoms from unit-cell atoms.

        Parameters
        ----------
        xyz_ia : coordinate/index
            Either a point in space or an index of an atom.
            If an index is passed it is the equivalent of passing
            the atomic coordinate `close_sc(self.xyz[xyz_ia,:])`.
        R      : (None), float/tuple of float
            The radii parameter to where the atomic connections are found.
            If ``R`` is an array it will return the indices:
            in the ranges:

            >>> ( x <= R[0] , R[0] < x <= R[1], R[1] < x <= R[2] ) # doctest: +SKIP

            If a single float it will return:

            >>> x <= R # doctest: +SKIP

        idx     : array_like, optional
            List of indices for atoms that are to be considered
        idx_xyz : array_like, optional
            The atomic coordinates of the equivalent ``idx`` variable (``idx`` must also be passed)
        ret_xyz : bool, optional
            If true this method will return the coordinates
            for each of the couplings.
        ret_rij : bool, optional
            If true this method will return the distances from the ``xyz_ia``
            for each of the couplings.
        """
        if R is None:
            R = self.maxR()
        R = ensure_array(R, np.float64)

        # Convert inedx coordinate to point
        if isinstance(xyz_ia, Integral):
            xyz_ia = self.xyz[xyz_ia, :]
        elif not isndarray(xyz_ia):
            xyz_ia = ensure_array(xyz_ia, np.float64)

        # Get global calls
        # Is faster for many loops
        concat = np.concatenate

        ret = [[np.empty([0], np.int32)] * len(R)]
        i = 0
        if ret_xyz:
            c = i + 1
            i += 1
            ret.append([np.empty([0, 3], np.float64)] * len(R))
        if ret_rij:
            d = i + 1
            i += 1
            ret.append([np.empty([0], np.float64)] * len(R))

        ret_special = ret_xyz or ret_rij

        def sphere_intersect(sc, s, c, r, up):

            # w = point - point-in-plane
            p1 = c - sc.offset(sc.sc_off[s, :])
            p2 = p1 - up

            # Check all 6 faces
            # See SuperCell.plane documentation for details
            n, _ = sc.plane(0, 1)
            if n[0] * p1[0] + n[1] * p1[1] + n[2] * p1[2] > r or \
               -n[0] * p2[0] - n[1] * p2[1] - n[2] * p2[2] > r:
                return False

            n, _ = sc.plane(0, 2)
            if n[0] * p1[0] + n[1] * p1[1] + n[2] * p1[2] > r or \
               -n[0] * p2[0] - n[1] * p2[1] - n[2] * p2[2] > r:
                return False
            n, _ = sc.plane(1, 2)
            if n[0] * p1[0] + n[1] * p1[1] + n[2] * p1[2] > r or \
               -n[0] * p2[0] - n[1] * p2[1] - n[2] * p2[2] > r:
                return False
            return True

        if np.all(self.sc.nsc == 1):
            def sphere_intersect(*args):
                return True

        # To reduce calculations of the same quantities
        up = self.sc.cell.sum(0)
        r = R[-1]

        for s in range(self.n_s):

            # Check if we need to process this supercell
            # Currently it seems this is overdoing it
            # I.e. this check is very heavy because it calculates
            # all planes
            if not sphere_intersect(self.sc, s, xyz_ia, r, up):
                continue

            na = self.na * s
            sret = self.close_sc(xyz_ia,
                self.sc.sc_off[s, :], R=R,
                idx=idx, idx_xyz=idx_xyz,
                ret_xyz=ret_xyz, ret_rij=ret_rij)

            if not ret_special:
                # This is to "fake" the return
                # of a list (we will do indexing!)
                sret = [sret]

            if isinstance(sret[0], list):
                # we have a list of arrays (len(R) > 1)
                for i, x in enumerate(sret[0]):
                    ret[0][i] = concat((ret[0][i], x + na), axis=0)
                    if ret_xyz:
                        ret[c][i] = concat((ret[c][i], sret[c][i]), axis=0)
                    if ret_rij:
                        ret[d][i] = concat((ret[d][i], sret[d][i]), axis=0)
            elif len(sret[0]) > 0:
                # We can add it to the list (len(R) == 1)
                # We add the atomic offset for the supercell index
                ret[0][0] = concat((ret[0][0], sret[0] + na), axis=0)
                if ret_xyz:
                    ret[c][0] = concat((ret[c][0], sret[c]), axis=0)
                if ret_rij:
                    ret[d][0] = concat((ret[d][0], sret[d]), axis=0)

        if len(R) == 1:
            if ret_xyz and ret_rij:
                return [ret[0][0], ret[1][0], ret[2][0]]
            elif ret_xyz or ret_rij:
                return [ret[0][0], ret[1][0]]
            return ret[0][0]

        if ret_special:
            return ret

        return ret[0]

    # Hence ``close_all`` has exact meaning
    # but ``close`` is shorten and retains meaning
    close_all = close

    def a2o(self, ia, all=False):
        """
        Returns an orbital index of the first orbital of said atom.
        This is particularly handy if you want to create
        TB models with more than one orbital per atom.

        Note that this will preserve the super-cell offsets.

        Parameters
        ----------
        ia : array_like
             Atomic indices
        all : bool, optional
             `False`, return only the first orbital corresponding to the atom,
             `True`, returns list of the full atom
        """
        ia = _a.asarrayi(ia)
        if not all:
            return self.firsto[ia % self.na] + (ia // self.na) * self.no
        off = (ia // self.na) * self.no
        ia = ia % self.na
        ob = self.firsto[ia] + off
        oe = self.lasto[ia] + off + 1

        # Create ranges
        if isinstance(ob, Integral):
            return _a.arangei(ob, oe)

        return array_arange(ob, oe)

    def o2a(self, io, uniq=False):
        """ Atomic index corresponding to the orbital indicies.

        This is a particurlaly slow algorithm due to for-loops.

        Note that this will preserve the super-cell offsets.

        Parameters
        ----------
        io: array_like
             List of indices to return the atoms for
        uniq : bool, optional
             If True only return the unique atoms.
        """
        if isinstance(io, Integral):
            if uniq:
                return np.unique(np.argmax(io % self.no <= self.lasto) + (io // self.no) * self.na)
            return np.argmax(io % self.no <= self.lasto) + (io // self.no) * self.na

        a = _a.asarrayi(io) % self.no
        # Use b-casting rules
        a.shape = (-1, 1)
        a = np.argmax(a <= self.lasto, axis=1)
        if uniq:
            return np.unique(a + (io // self.no) * self.na)
        return a + (io // self.no) * self.na

    def sc2uc(self, atom, uniq=False):
        """ Returns atom from super-cell indices to unit-cell indices, possibly removing dublicates """
        atom = ensure_dtype(atom)
        if uniq:
            return np.unique(atom % self.na)
        return atom % self.na
    asc2uc = sc2uc

    def osc2uc(self, orbs, uniq=False):
        """ Returns orbitals from super-cell indices to unit-cell indices, possibly removing dublicates """
        orbs = ensure_dtype(orbs)
        if uniq:
            return np.unique(orbs % self.no)
        return orbs % self.no

    def a2isc(self, ia):
        """
        Returns the super-cell index for a specific/list atom

        Returns a vector of 3 numbers with integers.
        """
        idx = ensure_dtype(ia) // self.na
        return self.sc.sc_off[idx, :]

    # This function is a bit weird, it returns a real array,
    # however, there should be no ambiguity as it corresponds to th
    # offset and "what else" is there to query?
    def a2sc(self, a):
        """
        Returns the super-cell offset for a specific atom
        """
        return self.sc.offset(self.a2isc(a))

    def o2isc(self, io):
        """
        Returns the super-cell index for a specific orbital.

        Returns a vector of 3 numbers with integers.
        """
        idx = ensure_dtype(io) // self.no
        return self.sc.sc_off[idx, :]

    def o2sc(self, o):
        """
        Returns the super-cell offset for a specific orbital.
        """
        return self.sc.offset(self.o2isc(o))

    def __plot__(self, fig_axes=False, axes=None, plot_sc=True, *args, **kwargs):
        """ Plot the geometry in a specified ``matplotlib.Axes`` object.

        Parameters
        ----------
        fig_axes : bool or matplotlib.Axes, optional
           the figure axes to plot in (if ``matplotlib.Axes`` object).
           If `True` it will create a new figure to plot in.
           If `False` it will try and grap the current figure and the current axes.
        axes : array_like, optional
           only plot a subset of the axis, defaults to all axes"
        plot_sc : bool, optional
           If `True` also plot the supercell structure
           only plot a subset of the axis, defaults to all axes"
        """
        # Default dictionary for passing to newly created figures
        d = dict()

        if plot_sc:
            self.sc.__plot__(fig_axes, axes, *args, **kwargs)
            if fig_axes is True:
                fig_axes = False

        if axes is None:
            axes = [0, 1, 2]

        # Ensure we have a new 3D Axes3D
        if len(axes) == 3:
            d['projection'] = '3d'

        if fig_axes is False:
            try:
                fig_axes = plt.mlibplt.gca()
            except Exception:
                fig_axes = plt.mlibplt.figure().add_subplot(111, **d)
        elif fig_axes is True:
            fig_axes = plt.mlibplt.figure().add_subplot(111, **d)

        colors = np.linspace(0, 1, num=len(self.atom.atom), endpoint=False)
        colors = colors[self.atom.specie]
        area = np.array([a.Z for a in self.atom.atom], np.float64)
        ma = np.min(area)
        area[:] *= 20 * np.pi / ma
        area = area[self.atom.specie]

        xyz = self.xyz.view()

        if isinstance(fig_axes, plt.mlib3d.Axes3D):
            # We should plot in 3D plots
            fig_axes.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], s=area, c=colors, alpha=0.8)
            plt.mlibplt.zlabel('Ang')
        else:
            fig_axes.scatter(xyz[:, axes[0]], xyz[:, axes[1]], s=area, c=colors, alpha=0.8)

        plt.mlibplt.xlabel('Ang')
        plt.mlibplt.ylabel('Ang')

    @classmethod
    def fromASE(cls, aseg):
        """ Returns geometry from an ASE object.

        Parameters
        ----------
        aseg : ASE ``Atoms`` object which contains the following routines:
            ``get_atomic_numbers``, ``get_positions``, ``get_cell``.
            From those methods a `sisl` object will be created.
        """
        Z = aseg.get_atomic_numbers()
        xyz = aseg.get_positions()
        cell = aseg.get_cell()
        # Convert to sisl object
        return cls(xyz, atom=Z, sc=cell)

    def toASE(self):
        """ Returns the geometry as an ASE ``Atoms`` object """
        from ase import Atoms
        return Atoms(symbols=self.atom.tolist(), positions=self.xyz.tolist(),
                     cell=self.cell.tolist())

    @property
    def mass(self):
        """ Returns the mass of all atoms as an array """
        return self.atom.mass

    def equal(self, other, R=True):
        """ Whether two geometries are the same (optional not check of the orbital radius)

        Parameters
        ----------
        other : Geometry
            the other Geometry to check against
        maxR : bool, optional
            if True also check if the orbital radii are the same (see `Atom.equal`)
        """
        if not isinstance(other, Geometry):
            return False
        same = self.sc == other.sc
        same = same and np.allclose(self.xyz, other.xyz)
        same = same and self.atom.equal(other.atom, R)
        return same

    def __eq__(self, other):
        return self.equal(other)

    def __ne__(self, other):
        return not (self == other)

    def sparserij(self, dtype=np.float64, na_iR=1000, method='rand'):
        """ Return the sparse matrix with all distances in the matrix

        The sparse matrix will only be defined for the elements which have
        orbitals overlapping with other atoms.

        Parameters
        ----------
        dtype : numpy.dtype, numpy.float64
           the data-type of the sparse matrix
        na_iR : int, 1000
           number of atoms within the sphere for speeding
           up the `iter_block` loop.
        method : str, 'rand'
           see `iter_block` for details

        Returns
        -------
        SparseAtom
           sparse matrix with all rij elements

        See Also
        --------
        iter_block : the method for looping the atoms
        distance : create a list of distances
        """
        rij = SparseAtom(self, nnzpr=20, dtype=dtype)

        # Get R
        R = (0.1, self.maxR())
        iR = self.iR(na_iR)

        # Do the loop
        for ias, idxs in self.iter_block(iR=iR, method=method):

            # Get all the indexed atoms...
            # This speeds up the searching for
            # coordinates...
            idxs_xyz = self[idxs, :]

            # Loop the atoms inside
            for ia in ias:
                idx, r = self.close(ia, R=R, idx=idxs, idx_xyz=idxs_xyz, ret_rij=True)
                rij[ia, idx[1]] = r[1]

        return rij

    def distance(self, atom=None, R=None, tol=0.1, method='average'):
        """ Calculate the distances for all atoms in shells of radius `tol` within ``max_R``

        Parameters
        ----------
        atom : int or array_like, optional
           only create list of distances from the given atoms, default to all atoms
        R : float, optional
           the maximum radius to consider, default to ``self.maxR()``.
           To retrieve all distances for atoms within the supercell structure
           you can pass `numpy.inf`.
        tol : float or array_like, optional
           the tolerance for grouping a set of atoms.
           This parameter sets the shell radius for each shell.
           I.e. the returned distances between two shells will be maximally
           `2*tol`, but only if atoms are within two consecutive lists.
           If this is a list, the shells will be of unequal size.

           The first shell size will be `tol * .5` or `tol[0] * .5` if `tol` is a list.

        method : {'average', 'mode', '<numpy.func>', func}
           How the distance in each shell is determined.
           A list of distances within each shell is gathered and the equivalent
           method will be used to extract a single quantity from the list of
           distances in the shell.
           If `'mode'` is chosen it will use `scipy.stats.mode`.
           If a string is given it will correspond to ``getattr(numpy, method)``,
           while any callable function may be passed. The passed function
           will only be passed a list of unsorted distances that needs to be
           processed.

        Examples
        --------
        >>> geom = Geometry([0]*3, Atom(1, R=1.), sc=SuperCell(1., nsc=[5, 5, 1]))
        >>> geom.distance() # use geom.maxR()
        array([ 1.])
        >>> geom.distance(tol=[0.5, 0.4, 0.3, 0.2])
        array([ 1.])
        >>> geom.distance(R=2, tol=[0.5, 0.4, 0.3, 0.2])
        array([ 1.        ,  1.41421356,  2.        ])
        >>> geom.distance(R=2, tol=[0.5, 0.7]) # the R = 1 and R = 2 ** .5 gets averaged
        array([ 1.20710678,  2.        ])

        Returns
        -------
        numpy.ndarray
           an array of positive numbers yielding the distances from the atoms in reduced form

        See Also
        --------
        sparserij : return a sparse matrix will all distances between atoms
        """

        # Correct atom input
        if atom is None:
            atom = _a.arangei(len(self))
        else:
            atom = ensure_array(atom)

        # Figure out maximum distance
        if R is None:
            R = self.maxR()
            if R < 0:
                raise ValueError((self.__class__.__name__ +
                                  ".distance cannot determine the `R` parameter. "
                                  "The internal `maxR()` is negative and thus not set. "
                                  "Set an explicit value for `R`."))
        else:
            maxR = 0.
            # These loops could be leveraged if we look at angles...
            for i, j, k in product([0, self.nsc[0] // 2],
                                   [0, self.nsc[1] // 2],
                                   [0, self.nsc[2] // 2]):
                if i == 0 and j == 0 and k == 0:
                    continue
                sc = [i, j, k]
                off = self.sc.offset(sc)

                for ii, jj, kk in product([0, 1], [0, 1], [0, 1]):
                    o = self.cell[0, :] * ii + \
                        self.cell[1, :] * jj + \
                        self.cell[2, :] * kk
                    maxR = max(maxR, np.sum((off + o) ** 2) ** 0.5)

            if R > maxR:
                R = maxR

        # Convert to list
        tol = ensure_array(tol, np.float64)
        if len(tol) == 1:
            # Now we are in a position to determine the sizes
            dR = _a.aranged(tol[0] * .5, R + tol[0] * .55, tol[0])
        else:
            dR = tol.copy()
            dR[0] *= 0.5
            # The first tolerance, is for it-self, the second
            # has to have the first tolerance as the field
            dR = _a.cumsumd(np.insert(dR, 1, tol[0]))

            if dR[-1] < R:
                # Now finalize dR by ensuring all remaining segments are captured
                t = tol[-1]

                dR = np.concatenate((dR, _a.aranged(dR[-1] + t, R + t * .55, t)))

            # Reduce to the largest value above R
            # This ensures that R, truly is the largest considered element
            dR = dR[:(dR > R).nonzero()[0][0]+1]

        # Now we can figure out the list of atoms in each shell
        # First create the initial lists of shell atoms
        # The inner shell will never be used, because it should correspond
        # to the atom it-self.
        shells = [[] for i in range(len(dR) - 1)]

        for a in atom:
            _, r = self.close(a, R=dR, ret_rij=True)

            for i, rlist in enumerate(r[1:]):
                shells[i].extend(rlist)

        # Now parse all of the shells with the correct routine
        # First we grap the routine:
        if isinstance(method, _str):
            if method == 'median':
                def func(lst):
                    return np.median(lst, overwrite_input=True)

            elif method == 'mode':
                from scipy.stats import mode
                def func(lst):
                    return mode(lst)[0]
            else:
                try:
                    func = getattr(np, method)
                except:
                    raise ValueError(self.__class__.__name__ + ".distance `method` has wrong input value.")
        else:
            func = method

        # Reduce lists
        for i in range(len(shells)):
            lst = shells[i]
            if len(lst) == 0:
                continue

            # Reduce elements
            shells[i] = func(lst)

        # Convert to flattened numpy array and ensure shape
        d = np.hstack(shells)
        d.shape = (-1,)

        return d

    # Create pickling routines
    def __getstate__(self):
        """ Returns the state of this object """
        d = self.sc.__getstate__()
        d['xyz'] = self.xyz
        d['atom'] = self.atom.__getstate__()
        return d

    def __setstate__(self, d):
        """ Re-create the state of this object """
        sc = SuperCell([1, 1, 1])
        sc.__setstate__(d)
        atoms = Atoms()
        atoms.__setstate__(d['atom'])
        self.__init__(d['xyz'], atom=atoms, sc=sc)

    @classmethod
    def _ArgumentParser_args_single(cls):
        """ Returns the options for `Geometry.ArgumentParser` in case they are the only options """
        return {'limit_arguments': False,
                'short': True,
                'positional_out': True,
            }

    # Hook into the Geometry class to create
    # an automatic ArgumentParser which makes actions
    # as the options are read.
    @default_ArgumentParser(description="Manipulate a Geometry object in sisl.")
    def ArgumentParser(self, p=None, *args, **kwargs):
        """ Create and return a group of argument parsers which manipulates it self `Geometry`.

        Parameters
        ----------
        parser: ArgumentParser, optional
           in case the arguments should be added to a specific parser. It defaults
           to create a new.
        limit_arguments: bool, optional
           If `False` additional options will be created which are similar to other options.
           For instance `--repeat-x` which is equivalent to `--repeat x`.
           Default `True`.
        short: bool, optional
           Create short options for a selected range of options.
           Default `False`.
        positional_out: bool, optional
           If `True`, adds a positional argument which acts as --out. This may be handy if only the geometry is in the argument list.
           Default `False`.
        """
        limit_args = kwargs.get('limit_arguments', True)
        short = kwargs.get('short', False)

        def opts(*args):
            if short:
                return args
            return [args[0]]

        # We limit the import to occur here
        import argparse

        # The first thing we do is adding the geometry to the NameSpace of the
        # parser.
        # This will enable custom actions to interact with the geometry in a
        # straight forward manner.
        d = {
            "_geometry": self.copy(),
            "_stored_geometry": False,
        }
        namespace = default_namespace(**d)

        # Create actions
        class Format(argparse.Action):

            def __call__(self, parser, ns, value, option_string=None):
                ns._geom_fmt = value[0]
        p.add_argument(*opts('--format'), action=Format, nargs=1, default='.8f',
                   help='Specify output format for coordinates.')

        class MoveOrigin(argparse.Action):

            def __call__(self, parser, ns, value, option_string=None):
                ns._geometry.xyz[:, :] -= np.amin(ns._geometry.xyz, axis=0)[None, :]
        p.add_argument(*opts('--origin', '-O'), action=MoveOrigin, nargs=0,
                   help='Move all atoms such that one atom will be at the origin.')

        class MoveCenterOf(argparse.Action):

            def __call__(self, parser, ns, value, option_string=None):
                xyz = ns._geometry.center(what='xyz')
                ns._geometry = ns._geometry.translate(ns._geometry.center(what=value) - xyz)
        p.add_argument(*opts('--center-of', '-co'), choices=['mass', 'xyz', 'position', 'cell'],
                       action=MoveCenterOf,
                       help='Move coordinates to the center of the designated choice.')

        class MoveUnitCell(argparse.Action):

            def __call__(self, parser, ns, value, option_string=None):
                if value in ['translate', 'tr', 't']:
                    # Simple translation
                    tmp = np.amin(ns._geometry.xyz, axis=0)
                    ns._geometry = ns._geometry.translate(-tmp)
                elif value in ['mod']:
                    g = ns._geometry
                    # Change all coordinates using the reciprocal cell and move to unit-cell (% 1.)
                    fxyz = g.fxyz % 1.
                    fxyz -= np.amin(fxyz, axis=0)
                    ns._geometry.xyz[:, :] = np.dot(fxyz, g.cell)
        p.add_argument(*opts('--unit-cell', '-uc'), choices=['translate', 'tr', 't', 'mod'],
                       action=MoveUnitCell,
                       help='Moves the coordinates into the unit-cell by translation or the mod-operator')

        # Rotation
        class Rotation(argparse.Action):

            def __call__(self, parser, ns, values, option_string=None):
                # Convert value[0] to the direction
                # The rotate function expects degree
                ang = angle(values[0], rad=False, in_rad=False)
                d = direction(values[1])
                if d == 0:
                    v = [1, 0, 0]
                elif d == 1:
                    v = [0, 1, 0]
                elif d == 2:
                    v = [0, 0, 1]
                ns._geometry = ns._geometry.rotate(ang, v)
        p.add_argument(*opts('--rotate', '-R'), nargs=2, metavar=('ANGLE', 'DIR'),
                       action=Rotation,
                       help='Rotate geometry around given axis. ANGLE defaults to be specified in degree. Prefix with "r" for input in radians.')

        if not limit_args:
            class RotationX(argparse.Action):

                def __call__(self, parser, ns, value, option_string=None):
                    # The rotate function expects degree
                    ang = angle(value, rad=False, in_rad=False)
                    ns._geometry = ns._geometry.rotate(ang, [1, 0, 0])
            p.add_argument(*opts('--rotate-x', '-Rx'), metavar='ANGLE',
                           action=RotationX,
                           help='Rotate geometry around first cell vector. ANGLE defaults to be specified in degree. Prefix with "r" for input in radians.')

            class RotationY(argparse.Action):

                def __call__(self, parser, ns, value, option_string=None):
                    # The rotate function expects degree
                    ang = angle(value, rad=False, in_rad=False)
                    ns._geometry = ns._geometry.rotate(ang, [0, 1, 0])
            p.add_argument(*opts('--rotate-y', '-Ry'), metavar='ANGLE',
                           action=RotationY,
                           help='Rotate geometry around second cell vector. ANGLE defaults to be specified in degree. Prefix with "r" for input in radians.')

            class RotationZ(argparse.Action):

                def __call__(self, parser, ns, value, option_string=None):
                    # The rotate function expects degree
                    ang = angle(value, rad=False, in_rad=False)
                    ns._geometry = ns._geometry.rotate(ang, [0, 0, 1])
            p.add_argument(*opts('--rotate-z', '-Rz'), metavar='ANGLE',
                           action=RotationZ,
                           help='Rotate geometry around third cell vector. ANGLE defaults to be specified in degree. Prefix with "r" for input in radians.')

        # Reduce size of geometry
        class ReduceSub(argparse.Action):

            def __call__(self, parser, ns, value, option_string=None):
                # Get atomic indices
                rng = lstranges(strmap(int, value))
                ns._geometry = ns._geometry.sub(rng)
        p.add_argument(*opts('--sub', '-s'), metavar='RNG',
                       action=ReduceSub,
                       help='Removes specified atoms, can be complex ranges.')

        class ReduceCut(argparse.Action):

            def __call__(self, parser, ns, values, option_string=None):
                s = int(values[0])
                d = direction(values[1])
                ns._geometry = ns._geometry.cut(s, d)
        p.add_argument(*opts('--cut', '-c'), nargs=2, metavar=('SEPS', 'DIR'),
                       action=ReduceCut,
                       help='Cuts the geometry into `seps` parts along the unit-cell direction `dir`.')

        # Swaps atoms
        class AtomSwap(argparse.Action):

            def __call__(self, parser, ns, value, option_string=None):
                # Get atomic indices
                a = lstranges(strmap(int, value[0]))
                b = lstranges(strmap(int, value[1]))
                if len(a) != len(b):
                    raise ValueError('swapping atoms requires equal number of LHS and RHS atomic ranges')
                ns._geometry = ns._geometry.swap(a, b)
        p.add_argument(*opts('--swap'), metavar=('A', 'B'), nargs=2,
                       action=AtomSwap,
                       help='Swaps groups of atoms (can be complex ranges). The groups must be of equal length.')

        # Add an atom
        class AtomAdd(argparse.Action):

            def __call__(self, parser, ns, values, option_string=None):
                # Create an atom from the input
                g = Geometry([float(x) for x in values[0].split(',')], atom=Atom(values[1]))
                ns._geometry = ns._geometry.add(g)
        p.add_argument(*opts('--add'), nargs=2, metavar=('COORD', 'Z'),
                       action=AtomAdd,
                       help='Adds an atom, coordinate is comma separated (in Ang). Z is the atomic number.')

        # Translate
        class Translate(argparse.Action):

            def __call__(self, parser, ns, values, option_string=None):
                # Create an atom from the input
                if ',' in values[0]:
                    xyz = [float(x) for x in values[0].split(',')]
                else:
                    xyz = [float(x) for x in values[0].split()]
                ns._geometry = ns._geometry.translate(xyz)
        p.add_argument(*opts('--translate', '-t'), nargs=1, metavar='COORD',
                       action=Translate,
                       help='Translates the coordinates via a comma separated list (in Ang).')

        # Periodicly increase the structure
        class PeriodRepeat(argparse.Action):

            def __call__(self, parser, ns, values, option_string=None):
                r = int(values[0])
                d = direction(values[1])
                ns._geometry = ns._geometry.repeat(r, d)
        p.add_argument(*opts('--repeat', '-r'), nargs=2, metavar=('TIMES', 'DIR'),
                       action=PeriodRepeat,
                       help='Repeats the geometry in the specified direction.')

        if not limit_args:
            class PeriodRepeatX(argparse.Action):

                def __call__(self, parser, ns, value, option_string=None):
                    ns._geometry = ns._geometry.repeat(int(value), 0)
            p.add_argument(*opts('--repeat-x', '-rx'), metavar='TIMES',
                           action=PeriodRepeatX,
                           help='Repeats the geometry along the first cell vector.')

            class PeriodRepeatY(argparse.Action):

                def __call__(self, parser, ns, value, option_string=None):
                    ns._geometry = ns._geometry.repeat(int(value), 1)
            p.add_argument(*opts('--repeat-y', '-ry'), metavar='TIMES',
                           action=PeriodRepeatY,
                           help='Repeats the geometry along the second cell vector.')

            class PeriodRepeatZ(argparse.Action):

                def __call__(self, parser, ns, value, option_string=None):
                    ns._geometry = ns._geometry.repeat(int(value), 2)
            p.add_argument(*opts('--repeat-z', '-rz'), metavar='TIMES',
                           action=PeriodRepeatZ,
                           help='Repeats the geometry along the third cell vector.')

        class PeriodTile(argparse.Action):

            def __call__(self, parser, ns, values, option_string=None):
                r = int(values[0])
                d = direction(values[1])
                ns._geometry = ns._geometry.tile(r, d)
        p.add_argument(*opts('--tile'), nargs=2, metavar=('TIMES', 'DIR'),
                       action=PeriodTile,
                       help='Tiles the geometry in the specified direction.')

        if not limit_args:
            class PeriodTileX(argparse.Action):

                def __call__(self, parser, ns, value, option_string=None):
                    ns._geometry = ns._geometry.tile(int(value), 0)
            p.add_argument(*opts('--tile-x', '-tx'), metavar='TIMES',
                           action=PeriodTileX,
                           help='Tiles the geometry along the first cell vector.')

            class PeriodTileY(argparse.Action):

                def __call__(self, parser, ns, value, option_string=None):
                    ns._geometry = ns._geometry.tile(int(value), 1)
            p.add_argument(*opts('--tile-y', '-ty'), metavar='TIMES',
                           action=PeriodTileY,
                           help='Tiles the geometry along the second cell vector.')

            class PeriodTileZ(argparse.Action):

                def __call__(self, parser, ns, value, option_string=None):
                    ns._geometry = ns._geometry.tile(int(value), 2)
            p.add_argument(*opts('--tile-z', '-tz'), metavar='TIMES',
                           action=PeriodTileZ,
                           help='Tiles the geometry along the third cell vector.')

        # Print some common information about the
        # geometry (to stdout)
        class PrintInfo(argparse.Action):

            def __call__(self, parser, ns, values, option_string=None):
                # We fake that it has been stored...
                ns._stored_geometry = True
                print(ns._geometry)
        p.add_argument(*opts('--info'), nargs=0,
                       action=PrintInfo,
                       help='Print, to stdout, some regular information about the geometry.')

        class Out(argparse.Action):

            def __call__(self, parser, ns, value, option_string=None):
                if value is None:
                    return
                if len(value) == 0:
                    return
                # If the vector, exists, we should write it
                kwargs = {}
                if hasattr(ns, '_geom_fmt'):
                    kwargs['fmt'] = ns._geom_fmt
                if hasattr(ns, '_vector'):
                    v = getattr(ns, '_vector')
                    if getattr(ns, '_vector_scale', True):
                        v /= np.max((v[:, 0]**2 + v[:, 1]**2 + v[:, 2]**2) ** .5)
                    kwargs['data'] = v
                ns._geometry.write(value[0], **kwargs)
                # Issue to the namespace that the geometry has been written, at least once.
                ns._stored_geometry = True
        p.add_argument(*opts('--out', '-o'), nargs=1, action=Out,
                       help='Store the geometry (at its current invocation) to the out file.')

        # If the user requests positional out arguments, we also add that.
        if kwargs.get('positional_out', False):
            p.add_argument('out', nargs='*', default=None, action=Out,
                           help='Store the geometry (at its current invocation) to the out file.')

        # We have now created all arguments
        return p, namespace


def sgeom(geom=None, argv=None, ret_geometry=False):
    """ Main script for sgeom.

    This routine may be called with `argv` and/or a `Sile` which is the geometry at hand.

    Parameters
    ----------
    geom : Geometry or BaseSile
       this may either be the geometry, as-is, or a `Sile` which contains
       the geometry.
    argv : list of str
       the arguments passed to sgeom
    ret_geometry : bool, optional
       whether the function should return the geometry
    """
    import sys
    import os.path as osp
    import argparse

    from sisl.io import get_sile, BaseSile

    # The geometry-file *MUST* be the first argument
    # (except --help|-h)

    # We cannot create a separate ArgumentParser to retrieve a positional arguments
    # as that will grab the first argument for an option!

    # Start creating the command-line utilities that are the actual ones.
    description = """
This manipulation utility is highly advanced and one should note that the ORDER of
options is determining the final structure. For instance:

   {0} geom.xyz --repeat x 2 --repeat y 2

is NOT equivalent to:

   {0} geom.xyz --repeat y 2 --repeat x 2

This may be unexpected but enables one to do advanced manipulations.

Additionally, in between arguments, one may store the current state of the geometry
by writing to a standard file.

   {0} geom.xyz --repeat y 2 geom_repy.xyz --repeat x 2 geom_repy_repx.xyz

will create two files:
   geom_repy.xyz
will only be repeated 2 times along the second lattice vector, while:
   geom_repy_repx.xyz
will be repeated 2 times along the second lattice vector, and then the first
lattice vector.
    """.format(osp.basename(sys.argv[0]))

    if argv is not None:
        if len(argv) == 0:
            argv = ['--help']
    elif len(sys.argv) == 1:
        # no arguments
        # fake a help
        argv = ['--help']
    else:
        argv = sys.argv[1:]

    # Ensure that the arguments have pre-pended spaces
    argv = cmd.argv_negative_fix(argv)

    p = argparse.ArgumentParser('Manipulates geometries from any Sile.',
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                description=description)

    # First read the input "Sile"
    if geom is None:
        argv, input_file = cmd.collect_input(argv)
        geom = get_sile(input_file).read_geometry()

    elif isinstance(geom, Geometry):
        # Do nothing, the geometry is already created
        pass

    elif isinstance(geom, BaseSile):
        geom = geom.read_geometry()
        # Store the input file...
        input_file = geom.file

    # Do the argument parser
    p, ns = geom.ArgumentParser(p, **geom._ArgumentParser_args_single())

    # Now the arguments should have been populated
    # and we will sort out if the input options
    # is only a help option.
    try:
        if not hasattr(ns, '_input_file'):
            setattr(ns, '_input_file', input_file)
    except:
        pass

    # Now try and figure out the actual arguments
    p, ns, argv = cmd.collect_arguments(argv, input=False,
                                        argumentparser=p,
                                        namespace=ns)

    # We are good to go!!!
    args = p.parse_args(argv, namespace=ns)
    g = args._geometry

    if not args._stored_geometry:
        # We should write out the information to the stdout
        # This is merely for testing purposes and may not be used for anything.
        print('Cell:')
        for i in (0, 1, 2):
            print('  {0:10.6f} {1:10.6f} {2:10.6f}'.format(*g.cell[i, :]))
        print('SuperCell:')
        print('  {0:d} {1:d} {2:d}'.format(*g.nsc))
        print(' {:>10s} {:>10s} {:>10s}  {:>3s}'.format('x', 'y', 'z', 'Z'))
        for ia in g:
            print(' {1:10.6f} {2:10.6f} {3:10.6f}  {0:3d}'.format(g.atom[ia].Z,
                                                                  *g.xyz[ia, :]))

    if ret_geometry:
        return g
    return 0
