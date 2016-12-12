"""
Testing suite.
Intended usage is either from shell with arguments, or interactive.
The normally questionable usage of globals allows resulting objects to
be manipulated interactively.

command line options:
    b: basicTest(), single particle animated in container
    s: animGenTest(n=4, ballsize=1.), four balls animated
    a: animGenTest(n=16, ballsize=0.25)
    p: physicsTest(num_balls=40), Compare pressure and temperature
    t: timingTest(), time things. This was just so I could decide what
        parameters to use
    c: conservationTest(5), check momentum and energy conservation 

"""
import sys

import objects
import system
import core

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def basicTest():
    """Animate a single ball in a container"""
    global ball1, ball2, mySys, fig, ax
    reload(objects)
    reload(system)
    # ball1 does circular motion because it looks cool
    # ball1 = objects.Ball(pos=[-10.99, 0, 0], vel=[0, 6, 0])
    ball2 = objects.Ball(pos=[-4, 0, 0], vel=[5, 1, 0])
    cont = objects.Container(12)
    # mySys = system.System([ball1], cont)
    mySys = system.System([ball2], cont)
    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax.axes.set_aspect('equal')
    mySys.init_system(ax)
    anim = animation.FuncAnimation(
        fig, mySys.next_frame,
        interval=20, blit=True
    )
    plt.show()


def subTest():
    global ball1, ball2, mySys, fig, ax
    reload(objects)
    reload(system)
    ball1 = objects.Ball()
    ball2 = objects.Ball(pos=[-4, 0, 0], vel=[1, 0, 0])
    cont = objects.Container(12)
    mySys = system.System([ball1, ball2], cont)
    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax.axes.set_aspect('equal')
    mySys.init_system(ax)
    plt.show()


def genTest(n=6):
    """To be used interactively. Generate system of *n* balls as mySys""" 
    global mySys
    reload(objects)
    reload(system)
    reload(core)
    balls = objects.distributeBalls(n, 12)
    cont = objects.Container(12.)
    mySys = system.System(balls, cont)


def animGenTest(n=6, r=12., ballsize=1.):
    """
    Create animation with *n* balls, size *ballsize* in container radius *r*
    """
    global mySys, fig, ax
    reload(objects)
    reload(system)
    reload(core)
    balls = objects.distributeBalls(n, r, ballsize=ballsize)
    cont = objects.Container(r)
    mySys = system.System(balls, cont)
    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax.axes.set_aspect('equal')
    mySys.init_system(ax)
    anim = animation.FuncAnimation(
        fig, mySys.next_frame,
        interval=20, blit=True
    )
    plt.show()


def physicsTest(num_balls=200, ballsize=0.01):
    global mySys, pressure
    sys.setrecursionlimit(10000)
    reload(objects)
    reload(system)
    reload(core)
    balls = objects.distributeBalls(
        n=num_balls, radius=12, ballsize=ballsize)
    cont = objects.Container(12)
    mySys = system.System(balls, cont)
    mySys.init_system(None)
    mySys.check_collide(5)
    P = mySys.pressure(20)
    print "pressure", P
    print "temp", mySys.temperature()
    core.logging.log(50, "temp is {}".format(mySys.temperature()))
    a = P * (4. / 3.) * np.pi * 12.**3
    b = num_balls * core.Kb * mySys.temperature()
    c = P * (((4. / 3.) * np.pi * 12.**3)
             - ((16. / 3.) * np.pi * ballsize**3 * num_balls)
             )
    print "Pv", a
    print "nkT", b
    print "frac", a / b
    print "P(V-bn)", c
    print "frac", c / b


def timingTest():
    """Time how long things take to decide how long to run things for"""
    for i in range(20, 200, 20):
        core.logging.log(20, "time is {}".format(core.time.strftime("%H%M%S")))
        core.logging.log(20, "i is {}".format(i))
        physicsTest(i)
    core.logging.log(20, "time is {}".format(core.time.strftime("%H%M%S")))


def conservationTest(step=5):
    """Run the system for *step* seconds to check physics works"""
    global mySys
    sys.setrecursionlimit(10000)
    reload(objects)
    reload(system)
    reload(core)
    balls = objects.distributeBalls(20, 12, ballsize=0.1)
    cont = objects.Container(12)
    mySys = system.System(balls, cont)
    mySys.init_system(None)
    E0 = mySys.total_KE()
    p0 = mySys.get_total_momentum()
    mySys.check_collide(step)
    E1 = mySys.total_KE()
    p1 = mySys.get_total_momentum()
    if core.close(p0, p1):
        core.logging.log(20, "Momentum conserved")
    else:
        core.logging.log(50, "Momentum not conserved")
        core.logging.log(50, p0)
        core.logging.log(50, p1)
    if np.abs(E0 - E1) < 1E-30:
        core.logging.log(20, "Energy conserved")
    else:
        core.logging.log(50, "Energy not conserved")
        core.logging.log(50, E0)
        core.logging.log(50, E1)


def brownTest():
    """Testing for brownian motion plot"""
    global mySys, fig, ax
    reload(objects)
    reload(system)
    reload(core)
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=core.FRAMERATE, bitrate=1800)
    balls = objects.distributeBalls(60, 5, ballsize=0.1, v=20.)
    big_ball = objects.BigBall(pos=[7,0,0], radius=1., mass=5)
    balls.append(big_ball)
    cont = objects.Container(9)
    mySys = system.System(balls, cont)
    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax.axes.set_aspect('equal')
    mySys.init_system(ax)
    anim = animation.FuncAnimation(
        fig, mySys.next_frame, frames=200,
        interval=20, blit=True, repeat=False
    )
    anim.save("mov.mp4", writer=writer)
    fig2 = plt.figure(2)
    ax2 = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax2.add_artist(plt.Circle((0, 0), 9, fill=False))
    nodes = big_ball.get_nodes()
    plt.plot(nodes[0], nodes[1])
    plt.savefig("brown.png")


def run(args):
    """Run the requested test function"""
    if args[1] == "b":
        basicTest()
    elif args[1] == "s":
        animGenTest(4, ballsize=1.)
    elif args[1] == "a":
        animGenTest(16, ballsize=0.25)
    elif args[1] == "p":
        physicsTest(num_balls=40)
    elif args[1] == "t":
        timingTest()
    elif args[1] == "c":
        conservationTest(5)


if __name__ == '__main__':
    Logger = core.logging.getLogger()
    args = sys.argv
    if len(args) == 1:
        Logger.setLevel(20)
        animGenTest(4)
    elif len(args) == 2:
        Logger.setLevel(20)
        run(args)
    elif len(args) == 3:
        if args[1] == "d":
            Logger.setLevel(int(args[2]))
            animGenTest(4)
        else:
            raise Exception("incorrect parameters")
    elif len(args) == 4:
        if args[2] == "d":
            Logger.setLevel(int(args[3]))
        else:
            raise Exception("incorrect parameters")
        run(args)
