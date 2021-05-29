import pygame

sign = lambda z: int(z/abs(z))

class Vector(object):
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def vector(self):
        return (self.x, self.y)

    @x.setter
    def x(self, new_x):
        self._x = new_x
    
    @y.setter
    def y(self, new_y):
        self._y = new_y

    def __repr__(self):
        return "<Vector: {}>".format(self.vector)
