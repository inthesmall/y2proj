# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:20:05 2016

@author: em1715
"""
import numpy as _np

import objects


class System:
    """Contain all the objects; keep track of time; trigger animation;
    calculate, queue and trigger collisions; calculate and store state
    variables.
    """

    def __init__(self, balls, container):
        """@todo include list of objects in the system.
        Maybe variable for next collision time and objects.
        time variable
        """
        # input checking
        self._balls = balls
        self._container = container
        self._objects = self._balls[:]
        self._objects.append(self._container)
        self._collisions = []
        None

    def init_figure(self):
        """@todo initialise animation"""
        colls = []
        for ball in self._balls:
            collTimes = []
            for obj in self._objects:
                if obj == ball: continue
                collTimes.append([ball.time_to_collision(obj), (ball, obj)])
                print collTimes
            colls.append(min(collTimes))
        colls.sort()
        print colls
        self._collisions = colls

    def next_frame(self):
        """@todo calls and renders next frame of animation.
        If the next collision occurs before the next frame, call collide
        instead.
        """
        None

    def collide(self):
        """@todo performs queued collision, then calculate and queue
        next collision"""
        None
