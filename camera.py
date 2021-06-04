import pygame
from util import Vector
from consts import Color

CAMERA_STEP = 1

class Camera(object):
    def __init__(self, window):
        self._window = window
        self._height = window.get_height()
        self._width = window.get_width()
        self._position = Vector(0, 0)
        # self._center = Vector(self._width//2, self._height//2)

    @property
    def window(self):
        return self._window

    @property
    def x(self):
        return self._position.x

    @property
    def y(self):
        return self._position.y

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def left_edge(self):
        return self._position.x

    @property
    def right_edge(self):
        return self._position.x + self._width

    @property
    def top_edge(self):
        return self._position.y

    @property
    def bottom_edge(self):
        return self._position.y + self._height

    @property
    def position(self):
        return self._position

    @property
    def center(self):
        return Vector(
            x = self._width/2,
            y = self._height/2
        )



    def display(self):
        pygame.draw.line(self.window, Color['Red'], (self.center.x - 10, self.center.y), (self.center.x + 10, self.center.y), 2)
        pygame.draw.line(self.window, Color['Red'], (self.center.x, self.center.y - 10), (self.center.x, self.center.y + 10), 2)

    def pan(self, movement_vector):
        assert isinstance(movement_vector, Vector)
        self._position += movement_vector
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x < 0:
            self.pan(Vector(CAMERA_STEP, 0))
        if keys[pygame.K_d]:
            self.pan(Vector(-CAMERA_STEP, 0))
