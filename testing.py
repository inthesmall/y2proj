import objects
import system
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


def animGenTest(n=6):
    global mySys, fig, ax
    reload(objects)
    reload(system)
    reload(core)
    balls = core.distributeBalls(n, 12, ballsize=0.25)
    cont = objects.Container(12.)
    mySys = system.System(balls, cont)
    # mySys._balls[0].setVel([20, 0, 0])
    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax.axes.set_aspect('equal')
    mySys.init_figure(ax)
    anim = animation.FuncAnimation(
        fig, mySys.next_frame,
        interval=20, blit=True
    )
    plt.show()


if __name__ == '__main__':
    animGenTest(25)
