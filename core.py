"""SOME DOCSTRING"""
import numpy as _np
import numpy.random as _rand
import logging
import time

import objects

logging.basicConfig(filename=time.strftime("%Y%m%d-%H%M%S") + ".log",
                    level=logging.DEBUG
                    )

FRAMERATE = 20.


def close(float1, float2=0.):
    """Determine if two floats are close enough to be equal. Return bool."""
    if abs(float1 - float2) <= 0.000001:
        return True
    else:
        return False


def distributeVelocities(n, v, dim):
    vx = 2 * v * (_rand.random(n) - 0.5)
    vy = 2 * v * (_rand.random(n) - 0.5)
    if dim == 3:
        vz = 2 * v * (_rand.random(n) - 0.5)
        vz -= _np.sum(vz) / n
        vz[0] -= _np.sum(vz)
    else:
        vz = _np.zeros(n)
    vx -= _np.sum(vx) / n
    vx[0] -= _np.sum(vx)
    vy -= _np.sum(vy) / n
    vy[0] -= _np.sum(vy)
    logging.debug("vx {}".format(vx))
    logging.debug("vy {}".format(vy))
    logging.debug("vz {}".format(vz))
    return vx, vy, vz


def distributeBalls(n, radius, ballsize=1, v=8., dim=2):
    """Arranges balls in a uniform grid with randomly distributed velocities

    Sum of velocities is zero.
    *v* is charcteristic velocity, not maximum due to implementation
    contraint.
    *dim* is number of dimensions for balls to have vel components in.
    2 for animation, 3 generally.
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
    vx, vy, vz = distributeVelocities(n=n, v=v, dim=dim)
    balls = []
    # number of balls already created
    ball = 0
    ballspace = side_len / per_row
    for row in xrange(per_row):
        for col in xrange(per_row):
            if ball < n:
                x = ((col + 0.5) * ballspace) - (side_len / 2)
                y = ((row + 0.5) * ballspace) - (side_len / 2)
                balls.append(objects.Ball(pos=[x, y, 0],
                                          vel=[vx[ball], vy[ball], vz[ball]],
                                          radius=ballsize
                                          ))
                ball += 1
            else:
                break
    return balls

