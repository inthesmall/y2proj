import sys

import core
import objects
import system

import matplotlib.pyplot as plt
import scipy.optimize as spo


sys.setrecursionlimit(100000)


def pressure(num_balls, ballsize, v, dim):
    balls = core.distributeBalls(
        n=num_balls, radius=12, ballsize=ballsize, v=v, dim=dim)
    cont = objects.Container(12)
    mySys = system.System(balls, cont)
    mySys.init_system(None)
    mySys.check_collide(5)
    P = mySys.pressure(20)
    T = mySys.temperature()
    return [P, T]


def genPVdata():
    res_2D = [[], [], [], []]
    res_3D = [[], [], [], []]
    for v in [2., 4]:  # range(2., 12., 2.):
        for num_balls in [20, 40, 60]:
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


def plotPV():
    res_2D, res_3D = genPVdata()
    plt.figure(1)
    NkT = [N * core.Kb * T for N, T in zip(res_2D[2], res_2D[1])]
    fit_2D = spo.curve_fit(lambda x, m: m * x, NkT, res_2D[0])
    fit_3D = spo.curve_fit(lambda x, m: m * x, NkT, res_3D[0])
    print fit_2D
    print fit_3D
    plt.plot(res_2D[0], NkT, 'bo', res_3D[0], NkT, 'ro')
    plt.show()
    print res_2D
    print res_3D
