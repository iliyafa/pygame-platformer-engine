from consts import Sides

class Collision(object):
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
    
    @property
    def triggered(self):
        return self.source.rect.colliderect(self.dest.rect)
    
    # def lookahead_y(self, dt):
    #     if self.source.right >= self.dest.left and self.source.left < self.dest.left or self.source.left <= self.dest.right and self.source.right > self.dest.right:
    #         # print((self.dest.top - (self.source.bottom + self.source.velocity.y*dt + self.source.acceleration.y*dt**2)))
    #         return abs(self.dest.top - (self.source.bottom + self.source.velocity.y*dt + self.source.acceleration.y*dt**2)) < epsilon
    #     return False

    @staticmethod
    def determine_side(source, dest):
        if source.rect.midtop[1] > dest.rect.midtop[1]:
            return Sides.TOP
        elif source.rect.midleft[0] > dest.rect.midleft[0]:
            return Sides.LEFT
        elif source.rect.midright[0] < dest.rect.midright[0]:
            return Sides.RIGHT
        else:
            return Sides.BOTTOM
