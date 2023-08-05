from __future__ import print_function

import numpy as np

# Import sile objects
from .sile import SileCDFSiesta
from ..sile import *

from sisl.unit.siesta import unit_convert
from sisl import Geometry, Atom, SuperCell, Grid
from sisl.physics import DensityMatrix
from sisl.physics import EnergyDensityMatrix
from sisl.physics import Hamiltonian


__all__ = ['ncSileSiesta']

Bohr2Ang = unit_convert('Bohr', 'Ang')
Ry2eV = unit_convert('Ry', 'eV')


class ncSileSiesta(SileCDFSiesta):
    """ Siesta file object """

    def read_supercell(self):
        """ Returns a SuperCell object from a Siesta.nc file
        """
        cell = np.array(self._value('cell'), np.float64)
        # Yes, this is ugly, I really should implement my unit-conversion tool
        cell *= Bohr2Ang
        cell.shape = (3, 3)

        nsc = np.array(self._value('nsc'), np.int32)

        return SuperCell(cell, nsc=nsc)

    def read_geometry(self):
        """ Returns Geometry object from a Siesta.nc file

        NOTE: Interaction range of the Atoms are currently not read.
        """

        # Read supercell
        sc = self.read_supercell()

        xyz = np.array(self._value('xa'), np.float64)
        xyz.shape = (-1, 3)

        if 'BASIS' in self.groups:
            bg = self.groups['BASIS']
            # We can actually read the exact basis-information
            b_idx = np.array(bg.variables['basis'][:], np.int32)

            # Get number of different species
            n_b = len(bg.groups)

            spc = [None] * n_b
            atm = dict()
            for basis in bg.groups:
                # Retrieve index
                ID = bg.groups[basis].ID
                atm['Z'] = int(bg.groups[basis].Atomic_number)
                # We could possibly read in R, however, that is not so easy?
                atm['mass'] = float(bg.groups[basis].Mass)
                atm['tag'] = basis
                atm['orbs'] = int(bg.groups[basis].Number_of_orbitals)
                spc[ID - 1] = Atom(**atm)
            atom = [None] * len(xyz)
            for ia in range(len(xyz)):
                atom[ia] = spc[b_idx[ia] - 1]
        else:
            atom = Atom(1)

        xyz *= Bohr2Ang

        # Create and return geometry object
        geom = Geometry(xyz, atom, sc=sc)
        return geom

    def _read_class_spin(self, cls, **kwargs):
        # Get the default spin channel
        spin = len(self._dimension('spin'))

        # First read the geometry
        geom = self.read_geometry()

        # Populate the things
        sp = self._crt_grp(self, 'SPARSE')
        v = sp.variables['isc_off']
        # pre-allocate the super-cells
        geom.sc.set_nsc(np.amax(v[:, :], axis=0) * 2 + 1)
        geom.sc.sc_off = v[:, :]

        # Now create the tight-binding stuff (we re-create the
        # array, hence just allocate the smallest amount possible)
        C = cls(geom, spin, nnzpr=1, orthogonal=False)

        C._csr.ncol = np.array(sp.variables['n_col'][:], np.int32)
        # Update maximum number of connections (in case future stuff happens)
        C._csr.ptr = np.insert(np.cumsum(C._csr.ncol, dtype=np.int32), 0, 0)
        C._csr.col = np.array(sp.variables['list_col'][:], np.int32) - 1

        # Copy information over
        C._csr._nnz = len(C._csr.col)
        C._csr._D = np.empty([C._csr.ptr[-1], spin+1], np.float64)
        C._csr._D[:, C.S_idx] = np.array(sp.variables['S'][:], np.float64)

        return C

    def read_hamiltonian(self, **kwargs):
        """ Returns a tight-binding model from the underlying NetCDF file """
        H = self._read_class_spin(Hamiltonian, **kwargs)
        S = H._csr._D[:, H.S_idx]

        Ef = float(self._value('Ef')[0]) * Ry2eV
        sp = self._crt_grp(self, 'SPARSE')

        for i in range(len(H.spin)):
            # Create new container
            h = np.array(sp.variables['H'][i, :], np.float64) * Ry2eV
            # Correct for the Fermi-level, Ef == 0
            if i < 2:
                h -= Ef * S[:]
            H._csr._D[:, i] = h[:]

        return H

    def read_hessian(self, **kwargs):
        """ Returns a tight-binding model from the underlying NetCDF file """
        H = self._read_class_spin(Hessian, **kwargs)

        sp = self._crt_grp(self, 'SPARSE')

        for i in range(sp.variables['H'].shape[0]):
            # Create new container
            H._csr._D[:, i] = sp.variables['H'][i, :] * Ry2eV ** 2

        return H

    def read_density_matrix(self, **kwargs):
        """ Returns a density matrix from the underlying NetCDF file """
        DM = self._read_class_spin(DensityMatrix, **kwargs)
        sp = self._crt_grp(self, 'SPARSE')
        for i in range(len(DM.spin)):
            # Create new container
            DM._csr._D[:, i] = sp.variables['DM'][i, :]

        return DM

    def read_energy_density_matrix(self, **kwargs):
        """ Returns energy density matrix from the underlying NetCDF file """
        EDM = self._read_class_spin(EnergyDensityMatrix, **kwargs)
        sp = self._crt_grp(self, 'SPARSE')
        for i in range(len(EDM.spin)):
            # Create new container
            EDM._csr._D[:, i] = sp.variables['EDM'][i, :] * Ry2eV

        return EDM

    def grids(self):
        """ Return a list of available grids in this file. """

        grids = []
        for g in self.groups['GRID'].variables:
            grids.expand(g)

        return grids

    def read_grid(self, name, spin=0):
        """ Reads a grid in the current Siesta.nc file

        Enables the reading and processing of the grids created by Siesta

        Parameters
        ----------
        name : str
           name of the grid variable to read
        spin : int
           the spin-index
        """
        # Swap as we swap back in the end
        geom = self.read_geometry().swapaxes(0, 2)

        # Shorthand
        g = self.groups['GRID']

        # Create the grid
        nx = len(g.dimensions['nx'])
        ny = len(g.dimensions['ny'])
        nz = len(g.dimensions['nz'])

        # Shorthand variable name
        v = g.variables[name]

        # Create the grid, Siesta uses periodic, always
        grid = Grid([nz, ny, nx], bc=Grid.PERIODIC, dtype=v.dtype)

        if len(v[:].shape) == 3:
            grid.grid = v[:, :, :]
        else:
            grid.grid = v[spin, :, :, :]

        try:
            u = v.unit
            if u == 'Ry':
                # Convert to ev
                grid *= Ry2eV
        except:
            # Allowed pass due to pythonic reading
            pass

        # Read the grid, we want the z-axis to be the fastest
        # looping direction, hence x,y,z == 0,1,2
        grid = grid.swapaxes(0, 2)
        grid.set_geom(geom)

        return grid

    def write_geometry(self, geom):
        """
        Creates the NetCDF file and writes the geometry information
        """
        sile_raise_write(self)

        # Create initial dimensions
        self._crt_dim(self, 'one', 1)
        self._crt_dim(self, 'n_s', np.prod(geom.nsc, dtype=np.int32))
        self._crt_dim(self, 'xyz', 3)
        self._crt_dim(self, 'no_s', np.prod(geom.nsc, dtype=np.int32) * geom.no)
        self._crt_dim(self, 'no_u', geom.no)
        self._crt_dim(self, 'na_u', geom.na)

        # Create initial geometry
        v = self._crt_var(self, 'nsc', 'i4', ('xyz',))
        v.info = 'Number of supercells in each unit-cell direction'
        v = self._crt_var(self, 'lasto', 'i4', ('na_u',))
        v.info = 'Last orbital of equivalent atom'
        v = self._crt_var(self, 'xa', 'f8', ('na_u', 'xyz'))
        v.info = 'Atomic coordinates'
        v.unit = 'Bohr'
        v = self._crt_var(self, 'cell', 'f8', ('xyz', 'xyz'))
        v.info = 'Unit cell'
        v.unit = 'Bohr'

        # Create designation of the creation
        self.method = 'sisl'

        # Save stuff
        self.variables['nsc'][:] = geom.nsc
        self.variables['xa'][:] = geom.xyz / Bohr2Ang
        self.variables['cell'][:] = geom.cell / Bohr2Ang

        # Create basis group
        bs = self._crt_grp(self, 'BASIS')

        # Create variable of basis-indices
        b = self._crt_var(bs, 'basis', 'i4', ('na_u',))
        b.info = "Basis of each atom by ID"

        orbs = np.empty([geom.na], np.int32)

        for ia, a, isp in geom.iter_species():
            b[ia] = isp + 1
            orbs[ia] = a.orbs
            if a.tag in bs.groups:
                # Assert the file sizes
                if bs.groups[a.tag].Number_of_orbitals != a.orbs:
                    raise ValueError(
                        'File ' +
                        self.file +
                        ' has erroneous data in regards of ' +
                        'of the already stored dimensions.')
            else:
                ba = bs.createGroup(a.tag)
                ba.ID = np.int32(isp + 1)
                ba.Atomic_number = np.int32(a.Z)
                ba.Mass = a.mass
                ba.Label = a.tag
                ba.Element = a.symbol
                ba.Number_of_orbitals = np.int32(a.orbs)

        # Store the lasto variable as the remaining thing to do
        self.variables['lasto'][:] = np.cumsum(orbs, dtype=np.int32)

    def write_hamiltonian(self, H, **kwargs):
        """ Writes Hamiltonian model to file

        Parameters
        ----------
        H : `Hamiltonian` model
           the model to be saved in the NC file
        Ef : double=0
           the Fermi level of the electronic structure (in eV)
        """
        if H.nnz == 0:
            raise ValueError(self.__class__.__name__ + '.write_hamiltonian + cannot write a Hamiltonian '
                             'with zero non-zero elements!')

        # Ensure finalizations
        H.finalize()

        # Ensure that the geometry is written
        self.write_geometry(H.geom)

        self._crt_dim(self, 'spin', len(H.spin))

        if H.dkind != 'f':
            raise NotImplementedError('Currently we only allow writing a floating point Hamiltonian to the Siesta format')

        v = self._crt_var(self, 'Ef', 'f8', ('one',))
        v.info = 'Fermi level'
        v.unit = 'Ry'
        v[:] = kwargs.get('Ef', 0.) / Ry2eV
        v = self._crt_var(self, 'Qtot', 'f8', ('one',))
        v.info = 'Total charge'
        v[:] = 0.
        if 'Qtot' in kwargs:
            v[:] = kwargs['Qtot']
        if 'Q' in kwargs:
            v[:] = kwargs['Q']

        # Append the sparsity pattern
        # Create basis group
        sp = self._crt_grp(self, 'SPARSE')

        self._crt_dim(sp, 'nnzs', H._csr.col.shape[0])
        v = self._crt_var(sp, 'n_col', 'i4', ('no_u',))
        v.info = "Number of non-zero elements per row"
        v[:] = H._csr.ncol[:]
        v = self._crt_var(sp, 'list_col', 'i4', ('nnzs',),
                          chunksizes=(len(H._csr.col),), **self._cmp_args)
        v.info = "Supercell column indices in the sparse format"
        v[:] = H._csr.col[:] + 1  # correct for fortran indices
        v = self._crt_var(sp, 'isc_off', 'i4', ('n_s', 'xyz'))
        v.info = "Index of supercell coordinates"
        v[:] = H.geom.sc.sc_off[:, :]

        # Save tight-binding parameters
        v = self._crt_var(sp, 'S', 'f8', ('nnzs',),
                          chunksizes=(len(H._csr.col),), **self._cmp_args)
        v.info = "Overlap matrix"
        if H.orthogonal:
            # We need to create the orthogonal pattern
            tmp = H._csr.copy(dims=[0])
            tmp.empty(keep_nnz=True)
            for i in range(tmp.shape[0]):
                tmp[i, i] = 1.

            if tmp.nnz != H.nnz:
                # We have added more stuff, something that we currently do not allow.
                raise ValueError(self.__class__.__name__ + '.write_hamiltonian '
                                 'is trying to write a Hamiltonian in Siesta format with '
                                 'not all on-site terms defined. Please correct. '
                                 'I.e. add explicitly *all* on-site terms.')

            v[:] = tmp._D[:, 0]
            del tmp
        else:
            v[:] = H._csr._D[:, H.S_idx]
        v = self._crt_var(sp, 'H', 'f8', ('spin', 'nnzs'),
                          chunksizes=(1, len(H._csr.col)), **self._cmp_args)
        v.info = "Hamiltonian"
        v.unit = "Ry"
        for i in range(len(H.spin)):
            v[i, :] = H._csr._D[:, i] / Ry2eV

        # Create the settings
        st = self._crt_grp(self, 'SETTINGS')
        v = self._crt_var(st, 'ElectronicTemperature', 'f8', ('one',))
        v.info = "Electronic temperature used for smearing DOS"
        v.unit = "Ry"
        v[:] = 0.025 / Ry2eV
        v = self._crt_var(st, 'BZ', 'i4', ('xyz', 'xyz'))
        v.info = "Grid used for the Brillouin zone integration"
        v[:] = np.identity(3) * 2
        v = self._crt_var(st, 'BZ_displ', 'i4', ('xyz',))
        v.info = "Monkhorst-Pack k-grid displacements"
        v.unit = "b**-1"
        v[:] = np.zeros([3], np.float64)

    def write_hessian(self, H, **kwargs):
        """ Writes Hessian model to file

        Parameters
        ----------
        H : `Hessian` model
           the model to be saved in the NC file
        """
        # Ensure finalizations
        H.finalize()

        # Ensure that the geometry is written
        self.write_geometry(H.geom)

        self._crt_dim(self, 'spin', 1)

        if H.dkind != 'f':
            raise NotImplementedError('Currently we only allow writing a floating point Hessian to the Siesta format')

        v = self._crt_var(self, 'Ef', 'f8', ('one',))
        v.info = 'Fermi level'
        v.unit = 'Ry'
        v[:] = 0.
        v = self._crt_var(self, 'Qtot', 'f8', ('one',))
        v.info = 'Total charge'
        v.unit = 'e'
        v[:] = 0.

        # Append the sparsity pattern
        # Create basis group
        sp = self._crt_grp(self, 'SPARSE')

        self._crt_dim(sp, 'nnzs', H._csr.col.shape[0])
        v = self._crt_var(sp, 'n_col', 'i4', ('no_u',))
        v.info = "Number of non-zero elements per row"
        v[:] = H._csr.ncol[:]
        v = self._crt_var(sp, 'list_col', 'i4', ('nnzs',),
                          chunksizes=(len(H._csr.col),), **self._cmp_args)
        v.info = "Supercell column indices in the sparse format"
        v[:] = H._csr.col[:] + 1  # correct for fortran indices
        v = self._crt_var(sp, 'isc_off', 'i4', ('n_s', 'xyz'))
        v.info = "Index of supercell coordinates"
        v[:] = H.geom.sc.sc_off[:, :]

        # Save tight-binding parameters
        v = self._crt_var(sp, 'S', 'f8', ('nnzs',),
                          chunksizes=(len(H._csr.col),), **self._cmp_args)
        v.info = "Overlap matrix"
        if H.orthogonal:
            # We need to create the orthogonal pattern
            tmp = H._csr.copy(dims=[0])
            tmp.empty(keep_nnz=True)
            for i in range(tmp.shape[0]):
                tmp[i, i] = 1.

            if tmp.nnz != H.nnz:
                # We have added more stuff, something that we currently do not allow.
                raise ValueError(self.__class__.__name__ + '.write_hamiltonian '
                                 'is trying to write a Hamiltonian in Siesta format with '
                                 'not all on-site terms defined. Please correct. '
                                 'I.e. add explicitly *all* on-site terms.')

            v[:] = tmp._D[:, 0]
            del tmp
        else:
            v[:] = H._csr._D[:, H.S_idx]
        v = self._crt_var(sp, 'H', 'f8', ('spin', 'nnzs'),
                          chunksizes=(1, len(H._csr.col)), **self._cmp_args)
        v.info = "Hessian"
        v.unit = "Ry**2"
        v[0, :] = H._csr._D[:, 0] / Ry2eV ** 2

        # Create the settings
        st = self._crt_grp(self, 'SETTINGS')
        v = self._crt_var(st, 'ElectronicTemperature', 'f8', ('one',))
        v.info = "Electronic temperature used for smearing DOS"
        v.unit = "Ry"
        v[:] = 0.025 / Ry2eV
        v = self._crt_var(st, 'BZ', 'i4', ('xyz', 'xyz'))
        v.info = "Grid used for the Brillouin zone integration"
        v[:] = np.identity(3) * 2
        v = self._crt_var(st, 'BZ_displ', 'i4', ('xyz',))
        v.info = "Monkhorst-Pack k-grid displacements"
        v.unit = "b**-1"
        v[:] = np.zeros([3], np.float64)

    def ArgumentParser(self, p=None, *args, **kwargs):
        """ Returns the arguments that is available for this Sile """
        newkw = Geometry._ArgumentParser_args_single()
        newkw.update(kwargs)
        return self.read_geometry().ArgumentParser(p, *args, **newkw)


add_sile('nc', ncSileSiesta)
