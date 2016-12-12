"""
Physics of a gas made of two different types of atoms

Should have been in physics.py but I didn't have a chance to finish
testing and getting results
"""
import sys

import core
import objects
import system

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo


def pressure(num_balls, ballsize, v, dim):
    balls = objects.distributeBalls(
        n=int(np.ceil(num_balls)),
        radius=12, ballsize=ballsize, v=v, dim=dim)
    for ball in balls[int(np.ceil(num_balls / 2.)):]:
        # Bad and wrong, but I don't want to write another method just
        # for a test.
        ball._radius = ballsize / 2.
    cont = objects.Container(12)
    mySys = system.System(balls, cont)
    mySys.init_system(None)
    mySys.check_collide(2)
    P = mySys.pressure(5)
    T = mySys.temperature()
    return [P, T]


def genPVdata(num_balls=60, ballsize=0.01):
    # res_2D = [[], [], [], []]
    res_3D = [[], [], [], []]
    for v in range(2, 22, 2):
        v = float(v)
        # i = pressure(num_balls=num_balls, ballsize=2., v=v, dim=2)
        # res_2D[0].append(i[0])
        # res_2D[1].append(i[1])
        # res_2D[2].append(num_balls)
        # res_2D[3].append(0.01)
        j = pressure(num_balls=num_balls, ballsize=ballsize, v=v, dim=3)
        res_3D[0].append(j[0])
        res_3D[1].append(j[1])
        res_3D[2].append(num_balls)
        res_3D[3].append(ballsize)
    return res_3D  # res_2D, res_3D


def plotPV(num_balls=27, ballsize=1.9):
    """
    Plot pressure against NkT with ideal and Van der Waals predictions

    Args:
        num_balls, int, number of balls
        ballsize, float, ball radius 
    """
    res_3D = genPVdata(num_balls, ballsize)
    plt.figure(1)
    # NkT_2D = [N * core.Kb * T for N, T in zip(res_2D[2], res_2D[1])]
    NkT_3D = [N * core.Kb * T for N, T in zip(res_3D[2], res_3D[1])]

    def linear(x, m):
        return x * m

    # fit_2D = spo.curve_fit(linear, NkT_2D, res_2D[0])
    fit_3D = spo.curve_fit(linear, res_3D[0], NkT_3D)
    # print fit_2D
    print fit_3D
    p = np.linspace(0, max(res_3D[0]), 200)  # need to add res_2D[0] to max
    expected_ideal = p * ((4. / 3.) * np.pi * 12.**3)
    line2 = plt.plot(p, expected_ideal, 'k-.', label="Ideal gas prediction")
    # line3 = plt.plot(res_2D[0], NkT_2D, 'bo', label="2D data")
    line4 = plt.plot(res_3D[0], NkT_3D, 'ro', label="3D data")
    plt.legend()
    plt.xlabel("Pressure in Pascals")
    plt.ylabel("NkT in Pascals per cubic meter")
    plt.show()
    # print res_2D
    print res_3D
