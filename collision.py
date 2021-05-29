import pygame
from enum import Enum, auto
pygame.init()

# Game Window Setting:
window = pygame.display.set_mode((1500, 900))

# epsilon = 1

VELOCITY_X = 1000
VELOCITY_Y = 0
GRAVITY = 5000

JUMP_VELOCITY = 1250

MAX_VELOCITY_X = 15000
MAX_VELOCITY_Y = 15000

# Colors:
Color = {
    "Blue"  : [0, 5, 141],
    "Green" : [40, 255, 0],
    "Red"   : [255, 15, 0],
    "Cyan"  : [174, 196, 255],
}
# Player = pygame.Rect(30, 30, 60, 60) # Player Rectangle (x on screen, y on screen(Above), x of rect, y of rect)

class Sides(Enum):
    TOP = auto(),
    BOTTOM = auto(),
    LEFT = auto(),
    RIGHT = auto(),
    UNKNOWN = auto()

# Obstacles:
obstacle_descriptors = [
    {'left': 0, 'top': 750, 'width': 1500, 'height': 150},
    {'left': 400, 'top': 650, 'width': 100, 'height': 100},
    {'left': 550, 'top': 600, 'width': 700, 'height': 50},
    {'left': 850, 'top': 450, 'width': 200, 'height': 50},
]

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


class Drawable(object):
    def __init__(self, window, color, x, y, width, height):
        self._window = window
        self._color = color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
    
    @property
    def rect(self):
        return pygame.Rect(self._x, self._y, self._width, self._height)

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

class Collision(object):
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
    
    @property
    def is_colliding(self):
        return self.source.rect.colliderect(self.dest.rect)
    
    # def lookahead_y(self, dt):
    #     if self.source.right >= self.dest.left and self.source.left < self.dest.left or self.source.left <= self.dest.right and self.source.right > self.dest.right:
    #         # print((self.dest.top - (self.source.bottom + self.source.velocity.y*dt + self.source.acceleration.y*dt**2)))
    #         return abs(self.dest.top - (self.source.bottom + self.source.velocity.y*dt + self.source.acceleration.y*dt**2)) < epsilon
    #     return False


def determine_side(source, dest):
        if source.rect.midtop[1] > dest.rect.midtop[1]:
            return Sides.TOP
        elif source.rect.midleft[0] > dest.rect.midleft[0]:
            return Sides.LEFT
        elif source.rect.midright[0] < dest.rect.midright[0]:
            return Sides.RIGHT
        else:
            return Sides.BOTTOM

class Player(Drawable):
    def __init__(self, window, color, x, y, width, height):
        super().__init__(window, color, x, y, width, height)
        self._velocity = Vector(0,VELOCITY_Y)
        self._acceleration = Vector(0, GRAVITY)
        self.is_jump = False
        self.on_floor = False

    @property
    def velocity(self):
        return self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    def move(self, dt):
        self._velocity.x = 0
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            if self.left > 0:
                self.velocity.x = -VELOCITY_X
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            if self.right < window.get_width():
                self.velocity.x = VELOCITY_X
        if keys[pygame.K_SPACE]:
            if self.on_floor:
                self.on_floor = False
                self.velocity.y -= JUMP_VELOCITY
        
    def update(self, dt):
        global end
        self.move(dt)
        self.velocity.y += self._acceleration.y*dt
        self._y += self.velocity.y*dt
        self.velocity.x += self._acceleration.x*dt
        self._x += self.velocity.x*dt

        collisions = []
        for obj in ENVIRONMENT:
            collision = Collision(self, obj)
            if collision.is_colliding:
                collisions.append(collision)
                # end = True
                # self.velocity.y = 0
                # self.acceleration.y = 0
                # end = True
                if obj.is_rigid:
                    self.on_floor = True
                    obj._color = Color['Green']
                    # print(self.acceleration)
                    self._y = obj.top - self.height + 1
                    self.velocity.y = 0
        
        if len(collisions) == 0:
            self.on_floor = False
        
        if self.on_floor:
            self.acceleration.y = 0
        else:
            self.acceleration.y = GRAVITY

            
        self.draw()

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect, 6, 1)

class Obstacle(Drawable):
    def __init__(self, window, color, left, top, width, height, is_rigid=True):
        super().__init__(window, color, left, top, width, height)
        self._velocity = Vector(0,0)
        self._is_rigid = is_rigid

    @property
    def velocity(self):
        return self._velocity
    
    @property
    def is_rigid(self):
        return self._is_rigid
    
    def set_color(self, color):
        self._color = color

    def update(self, dt):
        self.draw()

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect)

player = Player(window, Color['Red'], 530, 50, 60, 60)
obstacles = [Obstacle(window, Color['Blue'], **desc) for desc in obstacle_descriptors]
ENVIRONMENT = obstacles

def redrawGameWindow(dt):
    window.fill(0)
    for obj in ENVIRONMENT:
        obj.update(dt)
    player.update(dt)
    pygame.display.update()

clock = pygame.time.Clock()
FPS = 60
dt = 0.0
end = False

while not end:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        end = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True

    redrawGameWindow(dt)
    dt = clock.tick(FPS)/1000.0

pygame.quit()
exit()