# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:20:05 2016

@author: em1715
"""
# @todo STOP EACH COLLISION FROM HAPPENING TWICE!
import heapq

import objects
import core

import numpy as _np

from core import close, FRAMERATE, Kb


class System:
    """Contain all the objects; keep track of time; trigger animation;
    calculate, queue and trigger collisions; calculate and store state
    variables.
    """

    def __init__(self, balls, container):
        """Initialise the system with objects

        Args:
            balls: list, objects.Ball to include in system
            container: objects.Container for system
        """
        if type(balls) is not list:
            raise TypeError("balls is not of type list")
        if isinstance(container, objects.Container) is False:
            raise TypeError("container is not instance of Container")
        self._balls = balls
        self._container = container
        self._objects = self._balls[:]
        self._objects.append(self._container)
        self._collisions = []
        self._time = 0.
        self._frame = 0

    def init_system(self, figure):
        """Initialise system.

        Generate collisions heap. If animating, draw objects in their
        starting positions on *figure*

        Args:
        figure: matplotlib.pyplot.axes object. Axes to draw objects on.
            Pass None if not animating.
        """
        core.logging.log(10, "called init_func")
        ret = []
        for i, ball in enumerate(self._balls):
            self.next_collides(ball)

        if figure is not None:
            # draw the figures
            figure.add_artist(self._container.get_patch())
            for ball in self._balls:
                figure.add_patch(ball.get_patch())
                ret.append(ball.get_patch())
            core.logging.log(8,
                             "init returned collisions {}".format(
                                 self._collisions)
                             )
            return ret

    def next_frame(self, f):
        """Called by matplotlib.animation.FuncAnimation()

        Advance time to when frame *f* occurs, carry out any collisions
        on the way. Draw objects for frame *f*.
        Args:
            f: int, framenumber
        """
        core.logging.log(15, "called next_frame with frame {}".format(f))
        core.logging.log(15, "container momentum = {}".format(
            self._container.get_momentum()))
        patches = []
        self.check_collide()
        step = (f / FRAMERATE) - self._time
        self.tick(step)
        for ball in self._balls:
            patches.append(ball.get_patch())
        self._frame = f
        return patches

    def collide(self):
        """Perform next collision, then update the queue."""
        next_coll = heapq.heappop(self._collisions)
        obj1, obj2 = next_coll[1]
        obj1.collide(obj2)
        # First, recalculate for all the objects obj1 or obj2
        # collide with in the queue
        to_remove = []
        to_add = [obj1, obj2]
        for index, collision in enumerate(self._collisions):
            if obj1 in collision[1]:
                if obj2 in collision[1]:
                    to_remove.append(index)
                else:
                    # pick out the object that is not obj1
                    if not isinstance(obj1, objects.Container):
                        obj = [i for i in collision[1] if i is not obj1][0]
                        to_remove.append(index)
                        to_add.append(obj)
            elif obj2 in collision[1]:
                if not isinstance(obj2, objects.Container):
                    obj = [i for i in collision[1] if i is not obj2][0]
                    to_remove.append(index)
                    to_add.append(obj)
        # Then find what they actually collide with next
        for index in to_remove[::-1]:
            self._collisions.pop(index)
        heapq.heapify(self._collisions)
        for obj in to_add:
            self.next_collides(obj)

    def check_collide(self, end_t=0):
        """
        Check to see if two objects collide before *end_t* or next frame

        If the next collision occurs before *end_t* or next frame, call
        collide().
        If animating, pass *end_t* = 0.
        """
        core.logging.log(11, "self._collisions {}".format(self._collisions))
        t = self._time
        f = self._frame
        # time at the next frame
        if end_t == 0:
            t_1 = (f + 1) / FRAMERATE
        else:
            t_1 = end_t
        next_coll_t = self._collisions[0][0]
        if next_coll_t <= t_1:
            step = next_coll_t - t
            self.tick(step)
            self.collide()
            self.check_collide(end_t)
            return None
        else:
            return None

    def advance(self, step):
        t = self._time
        end_t = t + step
        self.check_collide(end_t)

    def tick(self, step):
        """Advances time by an increment *step*, in seconds"""
        # Stop the balls from sneaking inside each other due to rounding errors
        if step > 1E-10:
            step -= 1E-10
        for ball in self._balls:
            ball.move(step)
        self._time += step

    def next_collides(self, obj):
        """
        Find what an object next collides with, and add it to the queue
        """
        core.logging.log(8, "next_collides on {}".format(obj))
        if isinstance(obj, objects.Container):
            return None
        collTimes = []
        for other in self._objects:
            core.logging.log(8, "other is {}".format(other))
            if obj == other:
                core.logging.log(8, "continuing")
                continue
            time_to_coll = obj.time_to_collision(other)
            if time_to_coll is not None:
                if close(time_to_coll, 0) is False:
                    time_to_coll += self._time
                    collTimes.append(
                        [time_to_coll, (obj, other)]
                    )
            core.logging.log(8, "collTimes = {}".format(collTimes))
        if len(collTimes) > 0:
            heapq.heappush(self._collisions, min(collTimes))

    def total_KE(self):
        KE = 0
        for ball in self._balls:
            V2 = 0
            mass = ball.get_mass() * core.MASS
            vel = ball.get_vel()
            V2 = core._np.dot(vel, vel)
            KE += 0.5 * mass * V2
        return KE

    def mean_KE(self):
        KE = self.total_KE()
        return KE / len(self._balls)

    def temperature(self):
        return (2. / 3.) * self.mean_KE() / Kb

    def pressure(self, step):
        time = self._time
        end_t = time + step
        p0 = self._container.get_mag_momentum() * core.MASS
        print "p0 is", p0
        self.check_collide(end_t=end_t)
        p1 = self._container.get_mag_momentum() * core.MASS
        print "p1 is", p1
        t_remaining = (time + step) - self._time
        self.tick(t_remaining)
        dp = p1 - p0
        F = dp / step
        P = F / (4 * _np.pi * self._container.get_radius() ** 2)
        return P

    def get_total_momentum(self):
        p = 0
        for ball in self._balls:
            p += ball.get_mass() * ball.get_vel()
        p += self._container.get_momentum()
        return p
