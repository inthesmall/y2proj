# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:20:05 2016

@author: em1715
"""
import heapq
import numpy as _np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import objects

FRAMERATE = 50.


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

        Defines:
            self._balls: list of balls in system
            self._container: the container
            self._objects: All objects in system (balls + container)
            self._collisions: a heap of the next collisions with
                format [time_to_collision, (object1, object2)]
        """
        # input checking
        if type(balls) is not list:
            raise TypeError("balls is not of type list")
        if isinstance(container, objects.Container) is False:
            raise TypeError("container is not instance of Container")
        self._balls = balls
        self._container = container
        self._objects = self._balls[:]
        self._objects.append(self._container)
        self._collisions = []

    def init_figure(self, figure):
        """Generate starting collisions heap, then initialise animation.
        @todo initialise animation
        """
        ret = []
        for ball in self._balls:
            collTimes = []
            for other in self._objects:
                if other == ball:
                    continue
                time_to_coll = ball.time_to_collision(other)
                if time_to_coll is not None:
                    collTimes.append([time_to_coll, (ball, other)])
                # print collTimes
            heapq.heappush(self._collisions, min(collTimes))
        # draw the figures
        figure.add_artist(self._container.getPatch())
        for ball in self._balls:
            figure.add_patch(ball.getPatch())
            ret.append(ball.getPatch())
        return ret

    def next_frame(self, f):
        """Called by matplotlib.animation.FuncAnimation()

        @todo draws next frame of animation.
        If the next collision occurs before the next frame, call collide
        instead.
        Args:
            f: int, framenumber
        """
        patches = []
        step = self.check_collide(f)
        for ball in self._balls:
            ball.move(step)
            patches.append(ball.getPatch())
        return patches

    def collide(self):
        """@todo perform queued collision, then calculate and queue
        next collision"""
        next_coll = heapq.heappop(self._collisions)
        obj1, obj2 = next_coll[1]
        obj1.collide(obj2, True)
        for obj in [obj1, obj2]:
            if isinstance(obj, objects.Container):
                continue
            collTimes = []
            for other in self._objects:
                if obj == other:
                    continue
                time_to_coll = obj.time_to_collision(other)
                if time_to_coll is not None:
                    collTimes.append(
                        [obj.time_to_collision(other), (obj, other)]
                    )
            heapq.heappush(self._collisions, min(collTimes))

    def check_collide(self, f):
        """ """
        t = f / FRAMERATE
        dt = 1 / FRAMERATE
        next_coll_t = self._collisions[0][0]
        if next_coll_t <= t:
            step = dt - (t - next_coll_t)
            for ball in self._balls:
                ball.move(step)
            self.collide()
            ret = self.check_collide(f)
            return ret - step
        else:
            return dt
