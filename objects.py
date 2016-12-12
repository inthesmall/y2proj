"""
Contains object for use in System.

Defines:
    Ball, Class
    Container, Class
    BigBall, Class

    distributeBalls(n, radius, ballsize=1, v=8., dim=2), function,
        create Ball objects

Ethan Mills
@todo ellipse collisions
@todo finish ellipse container
@todo diatomic molecules
"""
import core

import matplotlib.pyplot as _plt
import numpy as _np
import numpy.random as _rand

from core import close


class Ball:
    """Ball class, represents a hard sphere in the system

    Methods:
        get_pos()
        get_vel()
        get_radius()
        get_mass()
        get_patch()
        set_pos(new_pos)
        set_vel(new_vel)
        move(step)
        time_to_collision(other)
        collide(other)
    """

    def __init__(self, mass=1, radius=1, pos=[0, 0, 0], vel=[0, 0, 0]):
        """Initialise Ball

        args:
            mass: float
            radius: float
            pos: numpy.array, 3 component Cartesian position vector
            vel: numpy.array, 3 component Cartesian velocity vector
        """

        # input checking
        if type(mass) not in (int, float):
            raise TypeError(
                "mass type {}, should be int or float".format(type(mass)))
        if mass < 0:
            raise ValueError(
                "mass is {}, should be positive or zero.".format(mass))
        if type(radius) not in (int, float):
            raise TypeError(
                "radius is type {}, should be int or float".format(
                    type(radius)))
        if radius <= 0:
            raise ValueError("radius is {}, should be positive".format(radius))
        if type(pos) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "pos is type {}, should be list or numpy array".format(
                    type(pos)))
        if len(pos) != 3:
            raise ValueError("pos has length {}, should be 3".format(len(pos)))
        if type(vel) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "vel is type {}, should be list or numpy array".format(
                    type(vel)))
        if len(vel) != 3:
            raise ValueError("vel has length {}, should be 3".format(len(vel)))

        self._mass = float(mass)
        self._radius = float(radius)
        self._pos = _np.array(pos)
        self._vel = _np.array(vel)
        self._patch = _plt.Circle(self._pos[:-1], self._radius)

    def __repr__(self):
        return ("""Ball(mass={0._mass}, radius={0._radius}, pos={0._pos},\
 vel={0._vel})""".format(self))

    def get_pos(self):
        """
        Return position as numpy array with 3 components [x, y, z]

        x, y, z are floats.
        """
        return self._pos

    def get_vel(self):
        """
        Return velocity as numpy array with 3 components [v_x, v_y, v_z]

        v_x, v_y, v_z are floats.
        """
        return self._vel

    def get_radius(self):
        """Return radius as a float"""
        return self._radius

    def get_mass(self):
        """Return mass as float"""
        return self._mass

    def get_patch(self):
        """Return matplotlib.pyplot.Circle representing Ball

        Circle centred on position of Ball, with radius equal to radius
        of Ball.
        """
        return self._patch

    def set_pos(self, new_pos):
        """Update position to *new_pos*

        *new_pos* is list or numpy.array: [x, y, z]; x, y, z are floats
        """
        # input checking
        if type(new_pos) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "new_pos is type {}, should be list or numpy array".format(
                    type(new_pos)))

        self._pos = _np.array(new_pos)
        self._patch.center = self._pos[:-1]

    def set_vel(self, new_vel):
        """Update position to *new_vel*

        *new_vel* is list or numpy.array: [v_x, v_y, v_z];
        v_x, v_y, v_z are floats
        """
        # input checking
        if type(new_vel) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "new_vel is type {}, should be list or numpy array".format(
                    type(new_vel)))

        self._vel = _np.array(new_vel)

    def move(self, step):
        """Move Ball to where it should be in *step* seconds

        *step* is float
        """
        # input checking
        if type(step) not in (int, float):
            raise TypeError(
                "step is type {}, should be int or float".format(type(step)))
        if step < 0:
            raise ValueError("step is {}, should be positive".format(step))

        pos = self.get_pos()
        vel = self.get_vel()
        new_pos = pos + (vel * step)
        self.set_pos(new_pos)

    def time_to_collision(self, other):
        """Return time until collision with *other* in seconds.

        *other* is Ball or Container.
        Retun time as float. If Ball does not collide with *other*,
        return None.
        """
        r1 = self.get_pos()
        core.logging.debug("r1 {}".format(r1))
        v1 = self.get_vel()
        core.logging.debug("v1 {}".format(v1))
        rad1 = self.get_radius()
        core.logging.debug("rad1 {}".format(rad1))
        r2 = other.get_pos()
        core.logging.debug("r2 {}".format(r2))
        v2 = other.get_vel()
        core.logging.debug("v2 {}".format(v2))
        rad2 = other.get_radius()
        core.logging.debug("rad2 {}".format(rad2))
        # Define a, b, c of the quadratic equation in dt
        a = _np.dot((v1 - v2), (v1 - v2))
        a = float(a)
        b = 2 * _np.dot((r1 - r2), (v1 - v2))
        b = float(b)
        c = _np.dot((r1 - r2), (r1 - r2)) - ((rad1 + rad2) * (rad1 + rad2))
        dt1 = (-b + _np.sqrt(_np.complex(b * b - 4 * a * c))) / (2 * a)
        dt2 = (-b - _np.sqrt(_np.complex(b * b - 4 * a * c))) / (2 * a)
        if _np.imag(dt1) != 0:
            return None
        minimum = min(dt1, dt2)
        if minimum > 0 and not close(minimum, 0):
            return float(minimum)
        maximum = max(dt1, dt2)
        if maximum > 0:
            return float(maximum)
        else:
            return None

    def collide(self, other):
        """Carry out collision with *other*

        *other* is Ball or Container.
        Update velocity of Ball and *other* as result of the collision.
        """
        Pos = self.get_pos()
        Vel = self.get_vel()
        Mass = self.get_mass()
        if isinstance(other, Container):
            r_norm = Pos / _np.sqrt(_np.dot(Pos, Pos))
            u_perp = _np.dot(Vel, r_norm) * r_norm
            v_para = Vel - u_perp
            v_perp = -u_perp
            dp = 2 * Mass * u_perp
            other.add_momentum(dp)
            v = v_perp + v_para
            self.set_vel(v)
        else:
            oPos = other.get_pos()
            oVel = other.get_vel()
            oMass = other.get_mass()

            r = oPos - Pos
            r = r / _np.sqrt(_np.dot(r, r))
            u1_perp = _np.dot(Vel, r) * r
            u2_perp = _np.dot(oVel, -r) * -r
            v1_para = Vel - u1_perp
            v2_para = oVel - u2_perp
            v1_perp = (((u1_perp * (Mass - oMass) + (2 * oMass * u2_perp))) /
                       (Mass + oMass))
            v2_perp = (((2 * Mass * u1_perp) + (u2_perp * (oMass - Mass))) /
                       (Mass + oMass))
            v1 = v1_perp + v1_para
            v2 = v2_perp + v2_para
            self.set_vel(v1)
            other.set_vel(v2)


class Container:
    """
    Spherical container for objects of type Ball. Has infinite mass.

    Methods:
        get_pos()
        get_vel()
        get_radius()
        get_patch()
        add_momentum(dp)
        get_momentum()
        get_mag_momentum()
    """

    def __init__(self, radius):
        """Initialise the container with parameters

        Args:
            radius: float. Radius of container.
        """
        # input checking
        if type(radius) not in (int, float):
            raise TypeError(
                "radius is type {}, should be int or float".format(
                    type(radius)))
        if radius <= 0:
            raise ValueError("radius is {}, should be positive".format(radius))

        self._radius = float(radius)
        self._patch = _plt.Circle((0, 0), self._radius, fill=False)
        self._momentum = _np.array([0., 0., 0.])
        self._mag_momentum = 0

    def __repr__(self):
        return """Container(radius=12)"""

    def __str__(self):
        return """(Container, radius = {}, momentum = {},
            mag_momentum = {})""".format(
            -self.get_radius(),
            self.get_momentum(),
            self.get_mag_momentum())

    def get_pos(self):
        """Return zero vector for use with collisions"""
        return _np.array([0, 0, 0])

    def get_vel(self):
        """Return zero vector for use with collisions"""
        return _np.array([0, 0, 0])

    def get_radius(self):
        """Return negative radius as float.

        Radius is negative to allow interoperability with standard
        Ball.time_to_collision()
        """
        return - self._radius

    def get_patch(self):
        """Return matplotlib.pyplot.Circle displaying Container"""
        return self._patch

    def add_momentum(self, dp):
        """Add momentum to container. *dp* is numpy.array"""
        # input checking
        if type(dp) not in (_np.array, _np.ndarray):
            raise TypeError(
                "dp is type {}, should be numpy.array".format(type(dp)))

        self._momentum += dp
        self._mag_momentum += _np.sqrt(_np.dot(dp, dp))

    def get_momentum(self):
        """Return momentum as numpy.array"""
        return self._momentum

    def get_mag_momentum(self):
        """Return magnitude of mometum as float"""
        return self._mag_momentum


class EllipticalContainer(Container):
    def __init__(self, radius, a, b):
        # @todo input checking
        # might not need radius
        Container.__init__(self, radius)
        self.a = a
        self.b = b

    def get_patch(self):
        """override Container.get_patch"""
        # @todo
        None

    def get_radius(self):
        """probably override Container.get_radius()"""
        None


class BigBall(Ball):
    """Large ball for use in brownian motion

    Extends Ball by tracking position nodes.
    methods:
        get_nodes: returns a list of positions where the velocity of
            BillBall changed
    """
    def __init__(self, mass=1, radius=1, pos=[0, 0, 0], vel=[0, 0, 0]):
        Ball.__init__(self, mass, radius, pos, vel)
        self._nodes = [[self.get_pos()[0]], [self.get_pos()[1]], [self.get_pos()[2]]]

    def set_vel(self, new_vel):
        """Extends Ball.set_vel to track nodes"""
        self._nodes[0].append(self.get_pos()[0])
        self._nodes[1].append(self.get_pos()[1])
        self._nodes[2].append(self.get_pos()[2])
        Ball.set_vel(self, new_vel)

    def get_nodes(self):
        """
        Return list of position vectors of points where velocity changed
        """
        return self._nodes

def _distributeVelocities(n, v, dim):
    vx = 2 * v * (_rand.random(n) - 0.5)
    vy = 2 * v * (_rand.random(n) - 0.5)
    if dim == 3:
        vz = 2 * v * (_rand.random(n) - 0.5)
        vz -= _np.sum(vz) / n
        # Account for rounding error
        vz[0] -= _np.sum(vz)
    else:
        vz = _np.zeros(n)
    vx -= _np.sum(vx) / n
    vx[0] -= _np.sum(vx)
    vy -= _np.sum(vy) / n
    vy[0] -= _np.sum(vy)
    core.logging.debug("vx {}".format(vx))
    core.logging.debug("vy {}".format(vy))
    core.logging.debug("vz {}".format(vz))
    return vx, vy, vz


def distributeBalls(n, radius, ballsize=1, v=8., dim=2):
    """Arranges balls in a uniform grid with randomly distributed velocities

    Sum of velocities is zero.
    *v* is characteristic velocity, approximately equal to v_max/sqrt(3)
    *dim* is number of dimensions for balls to have vel components in.
    2 for animation.
    """
    if type(n) not in (int, float):
        raise TypeError("n is type {}, should be int".format(type(n)))
    if n <= 0:
        raise ValueError("n has value {}, should be positive".format(n))
    if n % 1 != 0:
        raise ValueError("n is {}, should be an integer".format(n))
    if type(radius) not in (int, float):
        raise TypeError("radius has type {}, should be float")
    if type(ballsize) not in (int, float):
        raise TypeError(
            "ballsize has type {}, should be float".format(type(ballsize))
        )
    if ballsize <= 0:
        raise ValueError("ballsize is {}, should be positive".format(ballsize))
    # Container objects return a negative radius for collisions, we need
    # this to be positive
    radius = _np.abs(float(radius))
    if dim == 2:
        return _distributeBalls2D(n=n, radius=radius, ballsize=ballsize, v=v)
    elif dim == 3:
        return _distributeBalls3D(n=n, radius=radius, ballsize=ballsize, v=v)


def _distributeBalls2D(n, radius, ballsize, v):
    side_len = _np.sqrt(2) * radius
    per_row = int(_np.ceil(_np.sqrt(n)))
    if 2 * ballsize * per_row >= side_len:
        raise ValueError("Too many balls. Got {}".format(n))
    vx, vy, vz = _distributeVelocities(n=n, v=v, dim=2)
    balls = []
    # number of balls already created
    ball = 0
    ballspace = side_len / per_row
    for row in xrange(per_row):
        for col in xrange(per_row):
            if ball < n:
                x = ((col + 0.5) * ballspace) - (side_len / 2)
                y = ((row + 0.5) * ballspace) - (side_len / 2)
                balls.append(Ball(pos=[x, y, 0],
                                  vel=[vx[ball], vy[ball], vz[ball]],
                                  radius=ballsize
                                  ))
                ball += 1
            else:
                break
    return balls


def _distributeBalls3D(n, radius, ballsize, v):
    side_len = _np.sqrt(2) * radius
    print side_len
    per_row = int(_np.ceil(n**(1. / 3.)))
    print per_row
    if 2 * ballsize * per_row >= side_len:
        raise ValueError("Too many balls. Got {}".format(n))
    vx, vy, vz = _distributeVelocities(n=n, v=v, dim=3)
    balls = []
    # number of balls already created
    ball = 0
    ballspace = side_len / per_row
    for row in xrange(per_row):
        y = ((row + 0.5) * ballspace) - (side_len / 2)
        for col in xrange(per_row):
            x = ((col + 0.5) * ballspace) - (side_len / 2)
            for layer in xrange(per_row):
                if ball < n:
                    z = ((layer + 0.5) * ballspace) - (side_len / 2)
                    balls.append(Ball(pos=[x, y, z],
                                      vel=[vx[ball], vy[ball], vz[ball]],
                                      radius=ballsize
                                      ))
                    ball += 1
                else:
                    break
    return balls
