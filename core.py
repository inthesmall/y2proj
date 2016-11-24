"""SOME DOCSTRING"""
import numpy as _np


FRAMERATE = 50.


def close(float1, float2=0.):
    """Determine if two floats are close enough to be equal. Return bool."""
    if abs(float1 - float2) <= (100. * _np.finfo(float).eps):
        return True
    else:
        return False


def distributeBalls(n):
    """Arranges balls in a uniform grid with randomly distributed velocities

    Sum of velocities is zero.
    """
    return None