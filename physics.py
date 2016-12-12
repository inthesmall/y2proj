"""

"""
import sys

import core
import objects
import system

import matplotlib.animation as animation
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
    mySys.check_collide(2)
    P = mySys.pressure(5)
    T = mySys.temperature()
    return [P, T]


def genPVdata(num_balls=60, ballsize=0.01):
    # res_2D = [[], [], [], []]
    res_3D = [[], [], [], []]
    for v in range(2, 21, 1):
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
    p = np.linspace(0, max(res_3D[0]), 200) # need to add res_2D[0] to max
    expected_VdW = p * (((4. / 3.) * np.pi * 12**3) -
                        ((16. / 3.) * np.pi * ballsize**3 * num_balls))
    line1 = plt.plot(p, expected_VdW, 'g--', label="Van der Waals prediciton")
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


def genMaxwellBData(v=15.):
    # params
    rad = 12.
    ballsize = 0.2
    num_balls = 400

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
    """Plot speed distribution histrogram with M-B prediction"""
    vels, temp = genMaxwellBData(v=20.)
    print "temp", temp
    n, bins, patches = plt.hist(vels, bins=20, normed=True)
    print "n", n
    print "bins", bins
    v = np.linspace(0, bins[-1], 200)
    v2 = v * v
    y = np.sqrt(2 / np.pi) * (core.MASS / (core.Kb * temp))**(3. / 2.) \
        * v2 * np.exp(-core.MASS * v2 / (2 * core.Kb * temp))
    plt.plot(v, y, 'g--')
    plt.xlabel("Velocity")
    plt.ylabel("Probability")
    plt.show()


def brownGen():
    """Generate brownian motion animation and plot"""
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=core.FRAMERATE, bitrate=1800)
    balls = objects.distributeBalls(60, 5, ballsize=0.1, v=20.)
    big_ball = objects.BigBall(pos=[7, 0, 0], radius=1., mass=5)
    balls.append(big_ball)
    cont = objects.Container(9)
    mySys = system.System(balls, cont)
    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax.axes.set_aspect('equal')
    mySys.init_system(ax)
    anim = animation.FuncAnimation(
        fig, mySys.next_frame, frames=2000,
        interval=20, blit=True, repeat=False
    )
    anim.save("mov.mp4", writer=writer)
    fig2 = plt.figure(2)
    ax2 = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax2.add_artist(plt.Circle((0, 0), 9, fill=False))
    nodes = big_ball.get_nodes()
    plt.plot(nodes[0], nodes[1])
    plt.savefig("brown.png")