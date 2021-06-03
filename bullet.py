import pygame
from movable import Movable
from util import Vector

OFFSET_X = 10
OFFSET_Y = 10

BULLET_SPEED = 308.0

class Bullet(Movable):
    def __init__(self, color, character):
        self._character = character
        x = character.x + OFFSET_X
        y = character.y + OFFSET_Y
        width = 6
        height = 2
        velocity_y = 0
        print(BULLET_SPEED)
        print(self._character.direction)
        velocity_x = BULLET_SPEED * self._character.direction.value
        super().__init__(character.window, color, x, y, width, height, velocity=Vector(velocity_x, 0))
        self._visible = True
    
    @property
    def visible(self):
        return self._visible

    def move(self):
        if self.right > self.window.get_width() or self.left < 0:
            self._visible = False

    def draw(self):
        if self._visible:
            pygame.draw.rect(self.window, self.color, self.rect, 2, 1)

    def update(self, dt):
        self.move()
        print(self._x)
        print(self._character.direction)
        print(dt)

        self._x += self.velocity.x * dt
        self.draw()

    