# definition of cars

import pygame
import math

from pygame.transform import rotate

from images import CAR_1
from utils import blit_rotate_center, scale_image


class BaseCar:
    IMG = scale_image(CAR_1, 0.18)
    START_POS = (180, 200)

    def __init__(self, max_vel: float, rotation_vel: float) -> None:
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 90
        self.x, self.y = self.START_POS
        self.acceleration = 0.1


    def rotate(self, left = False, right = False) -> None:
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel


    def draw(self, window: pygame.display) -> None:
        blit_rotate_center(window, self.img, (self.x, self.y), self.angle)


    def move_forward(self) -> None:
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()


    def reverse(self) -> None:
        self.vel = max(-self.acceleration * 5, -self.max_vel / 3)
        self.move()


    def move(self) -> None:
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal


class PlayerCar(BaseCar):
    IMG = scale_image(CAR_1, 0.18)
    START_POS = (388, 755)


    def brake(self) -> None:
        self.vel = max(self.vel - self.acceleration, 0)
        self.move()


    def reduce_speed(self) -> None:
        self.vel = max(self.vel - self.acceleration / 3, 0)
        self.move()