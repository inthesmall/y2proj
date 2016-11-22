import objects
import system
import matplotlib.pyplot as plt


def test():
    global ball1, ball2, sys, fig, ax
    reload(objects)
    reload(system)
    ball1 = objects.Ball()
    ball2 = objects.Ball(pos=[-4, 0, 0], vel=[1, 0, 0])
    cont = objects.Container(12)
    sys = system.System([ball1, ball2], cont)
    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    ax.axes.set_aspect('equal')
    sys.init_figure(ax)
    plt.show()
