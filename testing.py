import objects
import system
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def mainTest():
    global ball1, ball2, mySys, fig, ax
    reload(objects)
    reload(system)
    ball1 = objects.Ball()
    ball2 = objects.Ball(pos=[-4, 0, 0], vel=[5, 0.1, 0])
    cont = objects.Container(12)
    mySys = system.System([ball1, ball2], cont)
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


if __name__ == '__main__':
    mainTest()
