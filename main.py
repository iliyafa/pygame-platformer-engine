from bullet import Bullet
import pygame

from consts import Direction, Sides, Color
from util import *
from drawable import Drawable
from collision import Collision
from bullet import Bullet

pygame.init()

# Game Window Setting:
window = pygame.display.set_mode((1500, 900))

# epsilon = 1

VELOCITY_X = 1000
VELOCITY_Y = 0
GRAVITY = 5000

JUMP_VELOCITY = 1250

BORDER_WIDTH = 6

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
        self.can_move = {
            "left": True,
            "right": True,
            "up": True,
            "down": True
        }
        self.direction = Direction.LEFT

    @property
    def velocity(self):
        return self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    def move(self, dt, pressed_key):
        self._velocity.x = 0
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.direction = Direction.LEFT
            if self.can_move['left'] and self.left >= BORDER_WIDTH:
                self.velocity.x = -VELOCITY_X
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.direction = Direction.RIGHT
            if self.can_move['right'] and self.right <= window.get_width() - BORDER_WIDTH:
                self.velocity.x = VELOCITY_X
        
        if pressed_key == pygame.K_SPACE:
            if self.on_floor and self.can_move['up']:
                self.on_floor = False
                self.velocity.y -= JUMP_VELOCITY
        
        if pressed_key == pygame.K_f:
            count = 0
            for b in bullets:
                if b.visible:
                    count += 1
            if count < 11:
                bullets.append(Bullet(
                    (255,255,0),
                    self
                ))
        
    def update(self, dt, pressed_key):
        global end
        self.move(dt, pressed_key)
        
        self.velocity.x += self._acceleration.x*dt
        self.velocity.y += self._acceleration.y*dt
        self._x += self.velocity.x*dt
        self._y += self.velocity.y*dt

        # if self.top > 0 and self.bottom < self.window.get_height():
        #     self._y += self.velocity.y*dt
        # else:
        #     self._y = 0 if self._y < 0 else self.window.get_height() - self.height - 1
        
        # if self.left > 0 and self.right < self.window.get_width():
        #     self._x += self.velocity.x*dt
        # else:
        #     self._x = 0 if self._x < 0 else self.window.get_width() - self.width + 1
        
        collisions = []
        colliding_sides = {
            Sides.BOTTOM: None,
            Sides.TOP: None,
            Sides.LEFT: None,
            Sides.RIGHT: None,
        }
        for obj in ENVIRONMENT:
            collision = Collision(self, obj)
            if collision.triggered:
                obj.is_colliding = True
                collisions.append(collision)
                colliding_sides[collision.determine_side(dt)] = collision
            else:
                obj.is_colliding = False
            
            if obj.is_colliding:
                obj._color = Color['Green']
            else:
                obj._color = Color['Blue']
        
        if len(collisions) == 0:
            self.on_floor = False
        else:
            if colliding_sides[Sides.RIGHT] is not None:
                obj = colliding_sides[Sides.RIGHT].dest
                self.can_move['right'] = False
                # if self.velocity.x > 0:
                self._x = obj.left - self.width + 1
                self.velocity.x = 0
            else:
                self.can_move['right'] = True
            
            if colliding_sides[Sides.LEFT] is not None:
                obj = colliding_sides[Sides.LEFT].dest
                self.can_move['left'] = False
                self._x = obj.right
                # if self.velocity.x > 0:
                self.velocity.x = 0
            else:
                self.can_move['left'] = True

            if colliding_sides[Sides.BOTTOM] is not None:
                obj = colliding_sides[Sides.BOTTOM].dest
                if self.velocity.y > 0:
                    self.on_floor = True
                    self.can_move['down'] = False
                    # print(self.acceleration)
                    self._y = obj.top - self.height + 1
                    self.velocity.y = 0
                    # self.acceleration.y = 0
            else:
                self.on_floor = False
                self.can_move['down'] = True
            
            if colliding_sides[Sides.TOP] is not None:
                obj = colliding_sides[Sides.TOP].dest
                self.can_move['up'] = False
                if self.velocity.y < 0:
                    self.velocity.y = 0
                    self._y = obj.bottom + 1
            else:
                self.can_move['up'] = True

                        

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
bullets = []
ENVIRONMENT = obstacles

def redrawGameWindow(dt, pressed_key):
    global bullets
    window.fill(0)
    for obj in ENVIRONMENT:
        obj.update(dt)
    for bullet in bullets:
        bullet.update(dt)
    
    count_visible = 0
    for bullet in bullets:
        if bullet.visible:
            count_visible += 1

    if count_visible == 0:
        bullets = []

    player.update(dt, pressed_key)
    pygame.display.update()

clock = pygame.time.Clock()
FPS = 60
dt = 0.0
end = False

while not end:
    pressed_key = None
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        end = True

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed_key = event.key
        if event.type == pygame.QUIT:
            end = True

    redrawGameWindow(dt, pressed_key)
    dt = clock.tick(FPS)/1000.0

pygame.quit()
exit()