import objects
import system
import sys
import core
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def mainTest():
    global ball1, ball2, mySys, fig, ax
    reload(objects)
    reload(system)
    ball1 = objects.Ball(pos=[-10.99, 0, 0], vel=[0, 6, 0])
    # ball2 = objects.Ball(pos=[-4, 0, 0], vel=[5, 0.1, 0])
    cont = objects.Container(12)
    mySys = system.System([ball1], cont)
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
    global mySys
    reload(objects)
    reload(system)
    reload(core)
    balls = core.distributeBalls(n, 12)
    cont = objects.Container(12.)
    mySys = system.System(balls, cont)


def animGenTest(n=6, r=12., ballsize=1.):
    global mySys, fig, ax
    reload(objects)
    reload(system)
    reload(core)
    balls = core.distributeBalls(n, r, ballsize=ballsize)
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
    balls = core.distributeBalls(
        n=num_balls, radius=12, ballsize=ballsize)
    cont = objects.Container(12)
    mySys = system.System(balls, cont)
    mySys.init_system(None)
    mySys.check_collide(5)
    P = mySys.pressure(20)
    print "pressure", P
    print "temp", mySys.temperature()
    core.logging.log(50, "temp is {}".format(mySys.temperature()))
    a = P * (4. / 3.) * core._np.pi * 12.**3
    b = num_balls * core.Kb * mySys.temperature()
    c = P * (((4. / 3.) * core._np.pi * 12.**3)
             - ((16. / 3.) * core._np.pi * ballsize**3 * num_balls)
             )
    print "Pv", a
    print "nkT", b
    print "frac", a / b
    print "P(V-bn)", c
    print "frac", c / b


def timingTest():
    for i in range(20, 200, 20):
        core.logging.log(20, "time is {}".format(core.time.strftime("%H%M%S")))
        core.logging.log(20, "i is {}".format(i))
        physicsTest(i)
    core.logging.log(20, "time is {}".format(core.time.strftime("%H%M%S")))


def conservationTest(step=5):
    global mySys
    sys.setrecursionlimit(10000)
    reload(objects)
    reload(system)
    reload(core)
    balls = core.distributeBalls(20, 12, ballsize=0.1)
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


def genPV():
    None


def run(args):
    """Run the requested test function"""
    if args[1] == "m":
        mainTest()
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
