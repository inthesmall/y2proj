# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:20:05 2016

@author: em1715
"""
import numpy as _np

import ball


class System:
    """Contain all the objects; keep track of time; trigger animation;
    calculate, queue and trigger collisions; calculate and store state
    variables.
    """

    def __init__(self):
        """@todo include list of objects in the system.
        Maybe variable for next collision time and objects.
        time variable
        """
        None

    def init_figure(self):
        """@todo initialise animation"""
        None

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
    """maybe define a tick() to increment time, and do the work of 
    calling collide or next_frame?"""