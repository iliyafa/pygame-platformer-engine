from util import sign, Vector
from consts import Sides

TOLERANCE = 20

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

    def determine_side(self, dt):
        # vel_x = self.source.velocity.x
        # lookahead = vel_x * dt

        # # Right:
        # for x in range(self.source.right.x, int(lookahead)):
        #     if self.dest.rect.collidepoint(Vector(x, self.source.right.y)):
        #         return Sides.RIGHT

        if (self.source.bottom - self.dest.top) < self.dest.height/2:
            return Sides.BOTTOM
        elif (self.dest.bottom - self.source.top) < self.dest.height/2:
            return Sides.TOP
        elif (self.source.right - self.dest.left) < self.dest.width/2:
            return Sides.RIGHT
        elif (self.dest.left - self.source.right) < self.dest.width/2:
            return Sides.LEFT
        else:
            return Sides.UNKNOWN