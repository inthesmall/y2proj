# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:20:05 2016

@author: em1715
"""
# @todo STOP EACH COLLISION FROM HAPPENING TWICE!
import heapq

import objects

from core import close, FRAMERATE


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

    def init_figure(self, figure):
        """
        Generate collisions heap, then draw objects in starting positions.

        Args:
        figure: matplotlib.pyplot.axes object. Axes to draw objects on.
        """
        print "called init_func"
        ret = []
        for i, ball in enumerate(self._balls):
            collTimes = []
            for other in self._objects[i:]:
                if other == ball:
                    continue
                time_to_coll = ball.time_to_collision(other)
                if time_to_coll is not None:
                    collTimes.append([time_to_coll, (ball, other)])
            if len(collTimes) > 0:
                heapq.heappush(self._collisions, min(collTimes))
        # draw the figures
        figure.add_artist(self._container.getPatch())
        for ball in self._balls:
            figure.add_patch(ball.getPatch())
            ret.append(ball.getPatch())
        print "init returned collisions", self._collisions
        return ret

    def next_frame(self, f):
        """Called by matplotlib.animation.FuncAnimation()

        Advance time to when frame *f* occurs, carry out any collisions
        on the way. Draw objects for frame *f*.
        Args:
            f: int, framenumber
        """
        # # DEBUGGING # #
        # print "next frame f =", f
        # for ball in self._balls:
        #     print "Begin ball:"
        #     print "vel =", ball.getVel()
        #     print "pos =", ball.getPos()
        #     print "End ball"
        # # /DEBUGGING # #
        print "called next_frame with frame", f
        patches = []
        self.check_collide()
        step = (f / FRAMERATE) - self._time
        self.tick(step)
        for ball in self._balls:
            patches.append(ball.getPatch())
        self._frame = f
        return patches

    def collide(self):
        """Perform next collision, then update the queue."""
        next_coll = heapq.heappop(self._collisions)
        obj1, obj2 = next_coll[1]
        obj1.collide(obj2, True)
        # First, recalculate for all the objects obj1 or obj2
        # collide with in the queue
        for index, collision in enumerate(self._collisions):
            if obj1 in collision[1]:
                if obj2 in collision[1]:
                    self._collisions.pop(index)
                else:
                    # pick out the object that is not obj1
                    if not isinstance(obj1, objects.Container):
                        obj = [i for i in collision[1] if i is not obj1][0]
                        self._collisions.pop(index)
                        heapq.heapify(self._collisions)
                        self.next_collides(obj)
            elif obj2 in collision[1]:
                if not isinstance(obj2, objects.Container):
                    obj = [i for i in collision[1] if i is not obj2][0]
                    self._collisions.pop(index)
                    heapq.heapify(self._collisions)
                    self.next_collides(obj)
        # Then find what they actually collide with next
        for obj in [obj1, obj2]:
            self.next_collides(obj)

    def check_collide(self):
        """Check to see if two objects collide before the next frame.

        If the next collision occurs before the next frame it will be
        executed.
        """
        print "self._collisions", self._collisions
        t = self._time
        f = self._frame
        # time at the next frame
        t_1 = (f + 1) / FRAMERATE
        dt = 1 / FRAMERATE
        next_coll_t = self._collisions[0][0]
        if next_coll_t <= t_1:
            step = next_coll_t - t
            self.tick(step)
            self.collide()
            self.check_collide()
            return None
        else:
            return None

    def tick(self, step):
        """Advances time by an increment *step*"""
        for ball in self._balls:
            ball.move(step)
        self._time += step

    def next_collides(self, obj):
        """
        Find what an object next collides with, and add it to the queue
        """
        print "next_collides on", obj
        if isinstance(obj, objects.Container):
            return None
        collTimes = []
        for other in self._objects:
            print "other is", other
            if obj == other:
                print "continuing"
                continue
            time_to_coll = obj.time_to_collision(other)
            if time_to_coll is not None:
                if close(time_to_coll, 0) is False:
                    time_to_coll += self._time
                    collTimes.append(
                        [time_to_coll, (obj, other)]
                    )
            print "collTimes =", collTimes
        if len(collTimes) > 0:
            heapq.heappush(self._collisions, min(collTimes))
