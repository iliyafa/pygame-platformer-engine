import math

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

    @x.setter
    def x(self, new_x):
        self._x = new_x
    
    @y.setter
    def y(self, new_y):
        self._y = new_y

    @property
    def as_tuple(self):
        return (self.x, self.y)

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)
    
    def __sub__(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y)

    def __mul__(self, vec):
        return sum([z[0]*z[1] for z in zip(self.as_tuple, vec.as_tuple)])
    
    def dot(self, vec):
        return self * vec
    
    def __repr__(self):
        return "<Vector: {}>".format(self.as_tuple)
