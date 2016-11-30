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
    mySys.init_figure(ax)
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
    mySys.init_figure(ax)
    plt.show()


def genTest(n=6):
    global mySys, fig, ax
    reload(objects)
    reload(system)
    reload(core)
    balls = core.distributeBalls(n, 12)
    cont = objects.Container(12.)
    mySys = system.System(balls, cont)
    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax.axes.set_aspect('equal')
    mySys.init_figure(ax)
    plt.show()


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
    mySys.init_figure(ax)
    anim = animation.FuncAnimation(
        fig, mySys.next_frame,
        interval=20, blit=True
    )
    plt.show()


def run(args):
    """Run the requested test function"""
    if args[1] == "m":
        mainTest()
    elif args[1] == "s":
        animGenTest(4, ballsize=1.)
    elif args[1] == "a":
        animGenTest(16, ballsize=0.25)


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
