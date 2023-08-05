"""Tests suite for XVSileSiesta
"""
from __future__ import print_function, division

from tempfile import mkstemp, mkdtemp

from sisl import Geometry, Atom, SuperCell
from sisl import Hamiltonian

import os.path as osp
import math as m
import numpy as np


def setUp(self):
    return self


def tearDown(self):
    return self


def setup(self):
    # Create temporary folder
    self.d = mkdtemp()
    alat = 1.42
    sq3h = 3.**.5 * 0.5
    C = Atom(Z=6, orbs=1, R=1.42)
    sc = SuperCell(np.array([[1.5, sq3h, 0.],
                             [1.5, -sq3h, 0.],
                             [0., 0., 10.]], np.float64) * alat,
                   nsc=[3, 3, 1])
    self.g = Geometry(np.array([[0., 0., 0.],
                                [1., 0., 0.]], np.float64) * alat,
                      atom=C, sc=sc)

    self.R = np.array([0.1, 1.5])
    self.t = np.array([0., 2.7])
    self.tS = np.array([(0., 1.0),
                        (2.7, 0.)])
    C = Atom(Z=6, orbs=1, R=max(self.R))
    sc = SuperCell(np.array([[1.5, sq3h, 0.],
                             [1.5, -sq3h, 0.],
                             [0., 0., 10.]], np.float64) * alat,
                   nsc=[3, 3, 1])
    self.gtb = Geometry(np.array([[0., 0., 0.],
                                [1., 0., 0.]], np.float64) * alat,
                      atom=C, sc=sc)

    self.ham = Hamiltonian(self.gtb)
    self.ham.construct([(0.1, 1.5), (0.1, 2.7)])


def teardown(self):
    # Do each removal separately
    try:
        shutil.rmtree(self.d)
    except:
        pass
