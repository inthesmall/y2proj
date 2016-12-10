"""
@todo Brownian motion
"""
import sys

import core
import objects
import system

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo


sys.setrecursionlimit(100000)


def pressure(num_balls, ballsize, v, dim):
    balls = objects.distributeBalls(
        n=num_balls, radius=12, ballsize=ballsize, v=v, dim=dim)
    cont = objects.Container(12)
    mySys = system.System(balls, cont)
    mySys.init_system(None)
    mySys.check_collide(5)
    P = mySys.pressure(20)
    T = mySys.temperature()
    return [P, T]


def genPVdata(num_balls=60):
    res_2D = [[], [], [], []]
    res_3D = [[], [], [], []]
    for v in [2, 4]:  # range(2, 12, 2):
        v = float(v)
        i = pressure(num_balls=num_balls, ballsize=0.01, v=v, dim=2)
        res_2D[0].append(i[0])
        res_2D[1].append(i[1])
        res_2D[2].append(num_balls)
        res_2D[3].append(0.01)
        j = pressure(num_balls=num_balls, ballsize=0.01, v=v, dim=3)
        res_3D[0].append(j[0])
        res_3D[1].append(j[1])
        res_3D[2].append(num_balls)
        res_3D[3].append(0.01)
    return res_2D, res_3D


def plotPV(num_balls=60):
    res_2D, res_3D = genPVdata()
    plt.figure(1)
    NkT_2D = [N * core.Kb * T for N, T in zip(res_2D[2], res_2D[1])]
    NkT_3D = [N * core.Kb * T for N, T in zip(res_3D[2], res_3D[1])]

    def linear(x, m):
        return x * m

    fit_2D = spo.curve_fit(linear, NkT_2D, res_2D[0])
    fit_3D = spo.curve_fit(linear, NkT_3D, res_3D[0])
    print fit_2D
    print fit_3D
    p = np.linspace(0, max(res_2D[0]), 200)
    expected_3D = p * (((4. / 3.) * np.pi * 12**3) -
                       ((16. / 3.) * np.pi * 0.01**3 * num_balls))
    plt.plot(p, expected_3D, 'g--')
    plt.plot(res_2D[0], NkT_2D, 'bo', res_3D[0], NkT_3D, 'ro')
    plt.xlabel("P")
    plt.ylabel("NkT")
    plt.show()
    print res_2D
    print res_3D


def genMaxwellBData(v=15.):
    # params
    rad = 12.
    ballsize = 0.2
    num_balls = 120

    # INITIALIZE SYSTEM
    balls = objects.distributeBalls(num_balls, rad, ballsize, v, 3)
    cont = objects.Container(rad)
    mySys = system.System(balls, cont)
    mySys.init_system(None)
    vels = []
    for ball in balls:
        v = ball.get_vel()
        vels.append(np.dot(v, v))
    v_bar = np.mean(vels)
    # 5 times charictersitic collision time
    t = 5. * ((4. / 3.) * np.pi * rad**3) / (
        np.sqrt(v_bar) * 4. * np.pi * ballsize**2 * num_balls)
    mySys.advance(t)
    vels = []
    for ball in balls:
        v = ball.get_vel()
        vels.append(np.sqrt(np.dot(v, v)))
    temp = mySys.temperature()
    return vels, temp


def plotMaxwellB():
    vels, temp = genMaxwellBData()
    print "temp", temp
    n, bins, patches = plt.hist(vels, bins=20, normed=True)
    print "n", n
    print "bins", bins
    v = np.linspace(0, bins[-1], 200)
    v2 = v * v
    y = np.sqrt(2 / np.pi) * (core.MASS / (core.Kb * temp))**(3. / 2.) \
        * v2 * np.exp(-core.MASS * v2 / (2 * core.Kb * temp))
    plt.plot(v, y, 'g--')
    plt.show()
