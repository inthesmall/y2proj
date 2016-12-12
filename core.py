"""Helper functions and logging

Defines:
    FRAMERATE, Int, Constant
    Kb, float, Constant, Boltzmann Constant
    MASS, float, Constant, scale factor for mass
    close(float1, float2=0), function,
        test for equality of floats and arrays
"""
import logging
import time

import numpy as _np


logging.basicConfig(filename=time.strftime("%Y%m%d-%H%M%S") + ".log",
                    level=20
                    )


FRAMERATE = 50.
Kb = 1.38064852E-23
MASS = 1.0E-26


def close(float1, float2=0.):
    """Determine if two floats are close enough to be equal. Return bool."""
    if type(float1) in (int, float) and type(float2) in (int, float):
        if abs(float1 - float2) <= 0.000001:
            return True
        else:
            return False
    elif (type(float1) in (_np.array, _np.ndarray) and
          type(float2) in (_np.array, _np.ndarray)):
        if abs(float1 - float2).all() <= 0.000001:
            return True
        else:
            return False
