import numpy as np

__all__ = ['Shape']


class Shape(object):
    """ Baseclass for shapes

    This class should always be sub-classed.

    There are a few routines that are *always* necessary
    to implement in a inherited class:

    `center`
      return the geometric center of the shape

    origo
      return the lowest left point in the shape

    volume
      return the volume of the shape.

    displacement
      return a vector that is the largest displacement vector such that
      a grid of the Shape will fully contian all space

    within
      Enables to check if coordinates, or other things
      are contained in this shape

    iwithin
      Returns only the indices of elements that are within

    enlarge
      Creates a new shape with a only the indices of elements that are within

    A `Shape` allows interaction with outside elements to check if geometric
    points are within the shapes.
    For instance to assert that a given point `x`, `y`, `z` is within a sphere
    of radius `r` with center `cx`, `cy`, `cz` on may do:

    This makes it very efficient to enable arbitrary shapes to be passed
    and used as determinations of regions of space.
    """

    def __init__(self, center):
        """ Initialize the Shape with a center """
        if center is None:
            self._center = np.zeros(3, np.float64)
        else:
            self._center = np.array(center, np.float64)

    def __call__(self, *args, **kwargs):
        """ Re-initialize the Shape """
        return self.__class__(*args, **kwargs)

    @property
    def origo(self):
        """ The geometric origo of the shape

        An origo should *always* be the lowest left coordinate of the shape.

        Notes
        -----
        Not all shapes have an origo. For instance a sphere only have a center,
        but an origo cannot be defined.
        """
        return None

    @property
    def center(self):
        """ The geometric center of the shape """
        return self._center

    @property
    def displacement(self):
        """ Return a displacement vector for full containment """
        raise NotImplementedError('displacement has not been implemented in: '+self.__class__.__name__)

    @property
    def volume(self):
        raise NotImplementedError('volume has not been implemented in: '+self.__class__.__name__)

    def enlarge(self, length):
        """ Return a new Shape with an increased size length """
        raise NotImplementedError('enlarge has not been implemented in: '+self.__class__.__name__)

    def within(self, other):
        """ Returns `True` if `other` is fully within `self` """
        raise NotImplementedError('__contains__ has not been implemented in: '+self.__class__.__name__)

    def iwithin(self, other):
        """ Returns indices of the elements of `other` that are within the shape """
        return self.within(other).nonzero()[0]

    def __contains__(self, other):
        return self.within(other)

    def __repr__(self):
        return self.__class__.__name__ + ' c({} {} {})'.format(*self.center)
