"""SOME DOCSTRING"""
import numpy as _np
import logging
import time

import objects

logging.basicConfig(filename=time.strftime("%Y%m%d-%H%M%S") + ".log",
                    level=logging.INFO
                    )

FRAMERATE = 50.


def close(float1, float2=0.):
    """Determine if two floats are close enough to be equal. Return bool."""
    if abs(float1 - float2) <= (100. * _np.finfo(float).eps):
        return True
    else:
        return False


def distributeBalls(n, radius, ballsize=1):
    """Arranges balls in a uniform grid with randomly distributed velocities

    Sum of velocities is zero.
    @todo implement velocity distribution
    """
    if type(n) not in (int, float):
        raise TypeError("n is type {}, should be int".format(type(n)))
    if n <= 0:
        raise ValueError("n has value {}, should be positive".format(n))
    if n % 1 != 0:
        raise ValueError("n is {}, should be an integer".format(n))
    if type(radius) not in (int, float):
        raise TypeError("radius has type {}, should be float")
    if type(ballsize) not in (int, float):
        raise TypeError(
            "ballsize has type {}, should be float".format(type(ballsize))
        )
    if ballsize <= 0:
        raise ValueError("ballsize is {}, should be positive".format(ballsize))
    # Container objects return a negative radius for collisions, we need
    # this to be positive
    radius = _np.abs(float(radius))
    side_len = _np.sqrt(2) * radius
    per_row = int(_np.ceil(_np.sqrt(n)))
    if 2 * ballsize * per_row >= side_len:
        raise ValueError("Too many balls. Got {}".format(n))
    balls = []
    ballspace = side_len / per_row
    for row in xrange(per_row):
        for col in xrange(per_row):
            if len(balls) < n:
                x = ((col + 0.5) * ballspace) - (side_len / 2)
                y = ((row + 0.5) * ballspace) - (side_len / 2)
                balls.append(objects.Ball(pos=[x, y, 0], vel=[0, 0, 0],
                                          radius=ballsize
                                          ))
            else:
                break
    return balls
