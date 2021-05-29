from util import sign
from consts import Sides

TOLERANCE = 15

class Collision(object):
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        self._collision_vector = self.source.center - self.dest.center
    
    @property
    def triggered(self):
        return self.source.rect.colliderect(self.dest.rect)
    
    @property
    def collision_vector(self):
        return self._collision_vector
    
    # def lookahead_y(self, dt):
    #     if self.source.right >= self.dest.left and self.source.left < self.dest.left or self.source.left <= self.dest.right and self.source.right > self.dest.right:
    #         # print((self.dest.top - (self.source.bottom + self.source.velocity.y*dt + self.source.acceleration.y*dt**2)))
    #         return abs(self.dest.top - (self.source.bottom + self.source.velocity.y*dt + self.source.acceleration.y*dt**2)) < epsilon
    #     return False

    def determine_side(self):
        if abs(self.source.bottom - self.dest.top) < TOLERANCE:
            return Sides.BOTTOM
        elif abs(self.dest.bottom - self.source.top) < TOLERANCE:
            return Sides.TOP
        elif abs(self.source.right - self.dest.left) < TOLERANCE:
            return Sides.RIGHT
        elif abs(self.dest.left - self.source.right) < TOLERANCE:
            return Sides.LEFT
        else:
            return Sides.UNKNOWN