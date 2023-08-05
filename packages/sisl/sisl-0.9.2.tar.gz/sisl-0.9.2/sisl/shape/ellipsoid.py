from math import pi
import numpy as np

import sisl._array as _a

from .base import Shape


__all__ = ['Ellipsoid', 'Spheroid', 'Sphere']


class Ellipsoid(Shape):
    """ 3D Ellipsoid shape

    Parameters
    ----------
    x : float
       the radius along x-direction
    y : float
       the radius along y-direction
    z : int
       the radius along z-direction

    Examples
    --------
    >>> xyz = [0, 2, 0]
    >>> shape = Ellipsoid(2, 2.2, 2, [0] * 3)
    >>> shape.within(xyz)
    array([ True], dtype=bool)
    """

    def __init__(self, x, y, z, center=None):
        super(Ellipsoid, self).__init__(center)
        self._radius = _a.arrayd([x, y, z])

    def __repr__(self):
        cr = np.array([self.center, self.radius])[:]
        return self.__class__.__name__ + ('{{c({0:.2f} {1:.2f} {2:.2f}) '
                                          'r({3:.2f} {4:.2f} {5:.2f})}}').format(*cr)

    @property
    def radius(self):
        """ Return the radius of the Ellipsoid """
        return self._radius

    @property
    def displacement(self):
        """ Return the displacement vector of the Ellipsoid """
        return self.radius * 0.5 ** 0.5 * 2

    @property
    def volume(self):
        """ Return the volume of the shape """
        return 4. / 3. * pi * np.product(self.radius)

    def expand(self, length):
        """ Return a new shape with a larger corresponding to `length` """
        r = self.radius + length
        return self(*r, center=self.center)

    def set_center(self, center):
        """ Change the center of the object """
        self.__init__(*self.radius, center=center)

    def within(self, other):
        """ Return whether the points are within the shape """

        if isinstance(other, (list, tuple)):
            other = _a.asarrayd(other)

        if not isinstance(other, np.ndarray):
            raise ValueError('Can not check other')

        other.shape = (-1, 3)

        idx = self.iwithin(other)
        within = np.empty(len(other), dtype='bool')
        within[:] = False
        within[idx] = True
        return within

    def iwithin(self, other):
        """ Return indices of the points that are within the shape """

        if isinstance(other, (list, tuple)):
            other = _a.asarrayd(other)

        if not isinstance(other, np.ndarray):
            raise ValueError('Could not index the other list')

        other.shape = (-1, 3)

        # First check
        fabs = np.fabs
        landr = np.logical_and.reduce
        r = self.radius
        tmp = other[:, :] - self.center[None, :]

        # Get indices where we should do the more
        # expensive exact check of being inside shape
        # I.e. this reduces the search space to the box
        r.shape = (1, 3)
        within = landr(fabs(tmp[:, :]) <= r, axis=1).nonzero()[0]

        # Now only check exactly on those that are possible candidates
        tmp = tmp[within, :]
        wtmp = (((tmp[:, :] / r) ** 2).sum(1) <= 1).nonzero()[0]

        # Ensure the shape of the internal radius is not changed
        r.shape = (3, )

        return within[wtmp]


class Spheroid(Ellipsoid):
    """ 3D spheroid shape

    Parameters
    ----------
    a : `float`
       the first spheroid axis radius
    b : `float`
       the second spheroid axis radius
    axis : `int`
       the symmetry axis of the Spheroid
    """

    def __init__(self, a, b, axis=2, center=None):
        if axis == 2: # z-axis
            super(Spheroid, self).__init__(a, a, b, center)
        elif axis == 1: # y-axis
            super(Spheroid, self).__init__(a, b, a, center)
        elif axis == 0: # x-axis
            super(Spheroid, self).__init__(b, a, a, center)
        else:
            raise ValueError('Symmetry axis of Spheroid must be `0 <= axis < 3`')

    def set_center(self, center):
        """ Change the center of the object """
        super(Spheroid, self).__init__(*self.radius, center=center)


class Sphere(Spheroid):
    """ Sphere """

    def __init__(self, radius, center=None):
        super(Sphere, self).__init__(radius, radius, center=center)

    def set_center(self, center):
        """ Change the center of the object """
        self.__init__(self.radius[0], center=center)

    def __repr__(self):
        return self.__class__.__name__ + '{{c({1:.2f} {2:.2f} {3:.2f}) r={0:.2f}}}'.format(self.radius[0], *self.center)
