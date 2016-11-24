# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 11:52:01 2016

@author: em1715
"""
import numpy as _np
import matplotlib.pyplot as _plt


def close(float1, float2=0.):
    """Determine if two floats are close enough to be equal. Return bool."""
    if abs(float1 - float2) <= (100. * _np.finfo(float).eps):
        return True
    else:
        return False


class Ball:
    """"""

    def __init__(self, mass=1, radius=1, pos=[0, 0, 0], vel=[0, 0, 0]):
        """"""

        # type checking
        if type(mass) not in (int, float):
            raise TypeError(
                "mass type {}, should be int or float".format(type(mass))
            )
        if mass < 0:
            raise ValueError(
                "mass is {}, should be positive or zero.".format(mass)
            )
        if type(radius) not in (int, float):
            raise TypeError(
                "radius is type {}, should be int or float".format(
                    type(radius)
                )
            )
        if radius <= 0:
            raise ValueError("radius is {}, should be positive".format(radius))
        if type(pos) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "pos is type {}, should be list or numpy array".format(
                    type(pos)
                )
            )
        if len(pos) != 3:
            raise ValueError("pos has length {}, should be 3".format(len(pos)))
        if type(vel) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "vel is type {}, should be list or numpy array".format(
                    type(vel)
                )
            )
        if len(vel) != 3:
            raise ValueError("vel has length {}, should be 3".format(len(vel)))

        self._mass = float(mass)
        self._radius = float(radius)
        self._pos = _np.array(pos)
        self._vel = _np.array(vel)
        self._patch = _plt.Circle(self._pos[:-1], self._radius)

    def getPos(self):
        """
        Return position as numpy array with 3 components [x, y, z]
        """
        return self._pos

    def getVel(self):
        """
        Return velocity as numpy array with 3 components [v_x, v_y, v_z]
        """
        return self._vel

    def getRadius(self):
        """Return radius as a float"""
        return self._radius

    def getMass(self):
        """ """
        return self._mass

    def getPatch(self):
        """ """
        return self._patch

    def setPos(self, new_pos):
        if type(new_pos) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "new_pos is type {}, should be list or numpy array".format(
                    type(new_pos)
                )
            )
        self._pos = _np.array(new_pos)
        self._patch.center = self._pos[:-1]

    def setVel(self, new_vel):
        if type(new_vel) not in (list, _np.array, _np.ndarray):
            raise TypeError(
                "new_vel is type {}, should be list or numpy array".format(
                    type(new_vel)
                )
            )
        self._vel = _np.array(new_vel)

    def move(self, step):
        if type(step) not in (int, float):
            raise TypeError(
                "step is type {}, should be int or float".format(type(step))
            )
        if step < 0:
            raise ValueError("step is {}, should be positive".format(step))
        pos = self.getPos()
        vel = self.getVel()
        new_pos = pos + (vel * step)
        self.setPos(new_pos)

    def time_to_collision(self, other):
        # @todo
        r1 = self.getPos()
        v1 = self.getVel()
        rad1 = self.getRadius()
        r2 = other.getPos()
        v2 = other.getVel()
        rad2 = other.getRadius()
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
        if minimum > 0:
            return float(minimum)
        maximum = max(dt1, dt2)
        if maximum > 0:
            return float(maximum)
        else:
            return None

    def collide(self, other, call=True):
        """Currently only works for Ball - Ball collisions.
        @todo: implement Container - Ball collisions
        """
        Pos = self.getPos()
        print "Pos =", Pos
        Vel = self.getVel()
        print "Vel =", Vel
        oMass = other.getMass()
        print "oMass =", oMass
        if oMass < 0:
            # Collided with container
            r_norm = Pos / _np.sqrt(_np.dot(Pos, Pos))
            u_perp = _np.dot(Vel, r_norm) * r_norm
            v_para = Vel - u_perp
            v_perp = -u_perp
            v = v_perp + v_para
            self.setVel(v)
        else:
            oPos = other.getPos()
            print "oPos =", oPos
            oVel = other.getVel()
            print "oVel =", oVel

            Mass = self.getMass()
            r = oPos - Pos
            print "r before norm =", r
            r = r / _np.sqrt(_np.dot(r, r))
            print "r after norm =", r
            u1_perp = _np.dot(Vel, r) * r
            print "u1_perp =", u1_perp
            u2_perp = _np.dot(oVel, -r) * -r
            print "u2_perp =", u2_perp
            v1_para = Vel - u1_perp
            print "v1_para =", v1_para
            v2_para = oVel - u2_perp
            print "v2_para =", v2_para
            v1_perp = ((u1_perp * (Mass - oMass) + (2 * oMass * u2_perp)) /
                       (Mass + oMass))
            v2_perp = ((2 * Mass * u1_perp) + (u2_perp * (oMass - Mass)) /
                       (Mass + oMass))
            print "v1_perp =", v1_perp
            print "v2_perp =", v2_perp
            v1 = v1_perp + v1_para
            v2 = v2_perp + v2_para
            self.setVel(v1)
            other.setVel(v2)


class Container:
    """"""

    def __init__(self, radius):
        if type(radius) not in (int, float):
            raise TypeError(
                "radius is type {}, should be int or float".format(
                    type(radius)
                )
            )
        if radius <= 0:
            raise ValueError("radius is {}, should be positive".format(radius))

        self._radius = float(radius)
        self._patch = _plt.Circle((0, 0), self._radius, fill=False)

    def getPos(self):
        """Return zero vector for use with collisions"""
        return _np.array([0, 0, 0])

    def getVel(self):
        """Return zero vector for use with collisions"""
        return _np.array([0, 0, 0])

    def getRadius(self):
        """Return negative radius as float.

        Radius is negative to allow interoperability with standard
        Ball.time_to_collision()
        """
        return - self._radius

    def getPatch(self):
        """ """
        return self._patch

    def getMass(self):
        return -1
