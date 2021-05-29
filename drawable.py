import pygame
from util import Vector

class Drawable(object):
    def __init__(self, window, color, x, y, width, height):
        self._window = window
        self._color = color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
    
    @property
    def vector(self):
        return Vector(self._x, self._y)
    
    @property
    def rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._height)
    
    @property
    def center(self):
        return Vector(*self.rect.center)
    
    @property
    def left(self):
        return self._x

    @property
    def right(self):
        return self._x + self._width - 1

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def top(self):
        return self._y

    @property
    def bottom(self):
        return self._y + self._height - 1

    @property
    def color(self):
        return self._color

    @property
    def window(self):
        return self._window
