from __future__ import print_function, division

import pytest

import math as m
import numpy as np

from sisl.shape.ellipsoid import *


@pytest.mark.shape
class TestEllipsoid(object):

    def test_create_ellipsoid(self):
        el = Ellipsoid(1., 1., 1.)
        el = Ellipsoid(1., 1., 1., [1.] * 3)
        el = Ellipsoid(1., 2., 3.)

    def test_create_spheroid(self):
        el = Spheroid(1., 1.)
        for i in range(3):
            el = Spheroid(1., 1., i)
        el = Spheroid(1., 1., center=[1.]*3)
        for i in range(3):
            el = Spheroid(1., 1., i, [1.]*3)

    def test_create_sphere(self):
        el = Sphere(1.)
        el = Sphere(1., center=[1.]*3)

    def test_expand1(self):
        e1 = Ellipsoid(1., 1., 1.)
        e2 = e1.expand(0.1)
        assert np.allclose(e1.radius + 0.1, e2.radius)

    def test_within1(self):
        o = Ellipsoid(1., 2., 3.)
        assert not o.within([-1.]*3)
        assert o.within([.2]*3)
        assert o.within([.5]*3)
        o = Spheroid(1., 2.)
        assert not o.within([-1.]*3)
        assert o.within([.2]*3)
        assert o.within([.5]*3)
        o = Sphere(1.)
        assert not o.within([-1.]*3)
        assert o.within([.2]*3)
        assert o.within([.5]*3)

    def test_iwithin1(self):
        o = Ellipsoid(1., 2., 3.)
        assert not o.iwithin([-1.]*3) == [0]
        assert o.iwithin([.2]*3) == [0]
        assert o.iwithin([.5]*3) == [0]
        o = Spheroid(1., 2.)
        assert not o.iwithin([-1.]*3) == [0]
        assert o.iwithin([.2]*3) == [0]
        assert o.iwithin([.5]*3) == [0]
        o = Sphere(1.)
        assert not o.iwithin([-1.]*3) == [0]
        assert o.iwithin([.2]*3) == [0]
        assert o.iwithin([.5]*3) == [0]
