import pygame

from consts import Sides, Color
from util import *
from drawable import Drawable
from collision import Collision

pygame.init()

# Game Window Setting:
window = pygame.display.set_mode((1500, 900))

# epsilon = 1

VELOCITY_X = 1000
VELOCITY_Y = 0
GRAVITY = 5000

JUMP_VELOCITY = 1250

# Obstacles:
obstacle_descriptors = [
    {'left': 0, 'top': 750, 'width': 1500, 'height': 150},
    {'left': 400, 'top': 650, 'width': 100, 'height': 100},
    {'left': 550, 'top': 600, 'width': 700, 'height': 50},
    {'left': 850, 'top': 450, 'width': 200, 'height': 50},
]


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
            if collision.triggered:
                collisions.append(collision)
                obj.is_colliding = True
                # end = True
                # self.velocity.y = 0
                # self.acceleration.y = 0
                # end = True
                if obj.is_rigid:
                    if self.velocity.y > 0:
                        self.on_floor = True
                        # print(self.acceleration)
                        self._y = obj.top - self.height + 1
                        self.velocity.y = 0
                    elif self.velocity.y < 0:
                        self.velocity.y = 0
                        self._y = obj.bottom + 1
            else:
                obj.is_colliding = False
            
            if obj.is_colliding:
                obj._color = Color['Green']
            else:
                obj._color = Color['Blue']
        
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
        self._is_rigid = is_rigid
        self._static_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self.is_colliding = False

    @property
    def rect(self):
        return self._static_rect
    
    @property
    def velocity(self):
        return Vector(0,0)
    
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