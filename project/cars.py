# definition of cars

import pygame
import math

from pygame import Mask, Surface

from images import CAR_1
from utils import blit_rotate_center

TRACK_HUNGARY_P1 = (390, 757)
TRACK_HUNGARY_P2 = (402, 746)
TRACK_HUNGARY_P3 = (414, 757)
TRACK_HUNGARY_P4 = (426, 746)
TRACK_HUNGARY_P5 = (438, 757)
TRACK_HUNGARY_P6 = (450, 746)
TRACK_HUNGARY_P7 = (462, 757)
TRACK_HUNGARY_P8 = (474, 746)
TRACK_HUNGARY_RESET_POSITION = (500, 755)


class BaseCar:
    IMG = CAR_1
    START_POS = TRACK_HUNGARY_P1
    MAX_VEL = 2.5
    ROTATION_VEL = 2.3

    def __init__(self, max_vel: float=MAX_VEL, rotation_vel: float=ROTATION_VEL) -> None:
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 90
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False) -> None:
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

    def collide(self, mask: Mask, x=0, y=0) -> tuple[int, int] | None:
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi


class PlayerCar(BaseCar):
    def __init__(
            self,
            max_vel: float=BaseCar.MAX_VEL,
            rotation_vel: float=BaseCar.ROTATION_VEL,
            img: Surface=BaseCar.IMG,
            start_pos: tuple[int, int]=BaseCar.START_POS
    ) -> None:
        super().__init__(max_vel, rotation_vel)

        self.img = img
        self.x, self.y = start_pos

    def brake(self) -> None:
        self.vel = max(self.vel - self.acceleration, 0)
        self.move()

    def reduce_speed(self) -> None:
        self.vel = max(self.vel - self.acceleration / 3, 0)
        self.move()

    def reset(self) -> None:
        self.x, self.y = TRACK_HUNGARY_RESET_POSITION
        self.angle = 90
        self.vel = 0


class ComputerCar(BaseCar):
    def __init__(
            self, max_vel: float=BaseCar.MAX_VEL,
            rotation_vel: float=BaseCar.ROTATION_VEL,
            img: Surface=BaseCar.IMG,
            start_pos: tuple[int, int]=TRACK_HUNGARY_P2,
            path=None
    ) -> None:
        super().__init__(max_vel, rotation_vel)

        if path is None:
            path = []

        self.path = path
        self.current_point = 0
        self.vel = max_vel
        self.img = img
        self.x, self.y = start_pos

    # helper function to draw points of computer car's path
    # def draw_points(self, window: pygame.display) -> None:
    #     for point in self.path:
    #         pygame.draw.circle(window, (255, 0, 0), point, 2)

    def draw(self, window: pygame.display) -> None:
        super().draw(window)

        # use of helper function
        # self.draw_points(window)

    def calculate_angle(self) -> None:
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)

        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self) -> None:
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self) -> None:
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()