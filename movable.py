import pygame
from util import *
from drawable import Drawable

class Movable(Drawable):
    def __init__(self, window, color, x, y, width, height, velocity=Vector(0,0), acceleration=Vector(0,0)):
        super().__init__(window, color, x, y, width, height)
        self._velocity = None
        self._acceleration = None

        if velocity is not None:
            assert isinstance(velocity, Vector), "Velocity must be a Vector"
            self._velocity = velocity
        
        if acceleration is not None:
            assert isinstance(acceleration, Vector), "Acceleration must be a Vector"
            self._acceleration = acceleration
        
    @property
    def velocity(self):
        return self._velocity
    
    @property
    def acceleration(self):
        return self._acceleration

    ### Setting individual axes can (and should) be done via `obj.(velocity|acceleration).(x|y) = {new_val}`
    @velocity.setter
    def velocity(self, new_vel):
        assert isinstance(new_vel, Vector), "Velocity must be a Vector"
        self._velocity = new_vel

    @acceleration.setter
    def acceleration(self, new_acc):
        assert isinstance(new_acc, Vector), "Acceleration must be a Vector"
        self._acceleration = new_acc
    
