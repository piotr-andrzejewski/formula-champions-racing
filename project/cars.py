# definition of cars

import pygame
import math
import numpy

from scipy.interpolate import CubicSpline
from pygame import Mask, Surface

from images import CAR_1
from utils import blit_rotate_center

TRACK_1_P1 = (380, 772)
TRACK_1_P2 = (400, 758.5)
TRACK_1_P3 = (420, 772)
TRACK_1_P4 = (440, 758.5)
TRACK_1_P5 = (460, 772)
TRACK_1_P6 = (480, 758.5)
TRACK_1_P7 = (500, 772)
TRACK_1_P8 = (520, 758.5)
TRACK_1_RESET_POSITION = (528.5, 758.5)

TRACK_1_PATH = [
    (234, 774), (71, 773), (26, 744), (96, 686), (200, 670),
    (332, 668), (377, 642), (363, 598), (286, 557), (241, 405),
    (211, 250), (169, 168), (74, 98), (105, 30), (182, 16), (290, 32),
    (328, 75), (416, 150), (492, 126), (554, 128), (598, 189),
    (658, 251), (751, 290), (774, 366), (766, 526), (759, 597),
    (730, 621), (650, 608), (582, 610), (550, 647), (622, 675),
    (694, 672), (746, 705), (723, 767), (624, 778), (455, 773)
]
TRACK_1_PATH_POINT_MARGIN = 2

class BaseCar:
    IMG = CAR_1
    START_POS = TRACK_1_P1
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
        self.x, self.y = TRACK_1_RESET_POSITION
        self.angle = 90
        self.vel = 0


class ComputerCar(BaseCar):
    def __init__(
            self, max_vel: float=BaseCar.MAX_VEL,
            img: Surface=BaseCar.IMG,
            start_pos: tuple[int, int]=TRACK_1_P2
    ) -> None:
        super().__init__(max_vel)

        self.path = TRACK_1_PATH
        self.current_point = 0
        self.vel = max_vel
        self.img = pygame.transform.rotate(img, -90)
        self.x, self.y = start_pos
        self.smooth_direction = (0, 0)

    def move_towards(self, target_x: float, target_y: float) -> None:
        # calculate the direction vector and distance
        direction = (target_x - self.x, target_y - self.y)
        distance = math.hypot(*direction)

        if distance != 0:
            direction = (direction[0] / distance, direction[1] / distance)
            self.angle = math.degrees(math.atan2(-direction[1], direction[0]))

        # adjust smoothness of direction change
        smooth_factor = 0.095
        self.smooth_direction = (
            self.smooth_direction[0] + smooth_factor * (direction[0] - self.smooth_direction[0]),
            self.smooth_direction[1] + smooth_factor * (direction[1] - self.smooth_direction[1])
        )

        # move towards the target
        self.x += self.smooth_direction[0] * self.vel
        self.y += self.smooth_direction[1] * self.vel

    def update_path_point(self, smooth_path: list[tuple[float, float]]) -> None:
        if self.current_point < len(smooth_path):
            target_x, target_y = smooth_path[self.current_point]
            self.move_towards(target_x, target_y)

            # checking if hypotenuse is smaller than desired margin to move to the next path point
            if math.hypot(target_x - self.x, target_y - self.y) < TRACK_1_PATH_POINT_MARGIN:
                self.current_point += 1

    def draw(self, window: pygame.display) -> None:
        self.update_path_point(self.smooth_path())
        super().draw(window)

        # # use of helper function to display path points
        # self.draw_points(window)

    # function to interpolate path with cubic splines to make more smooth path to follow
    def smooth_path(self) -> list[tuple[float, float]]:
        # extract x and y coordinates from points in path
        pos_x, pos_y = zip(*self.path)

        points = numpy.linspace(0, 1, len(self.path))
        cubic_spline_x = CubicSpline(points, pos_x)
        cubic_spline_y = CubicSpline(points, pos_y)
        smooth_points = numpy.linspace(0, 1, 100)

        return list(zip(cubic_spline_x(smooth_points), cubic_spline_y(smooth_points)))

    # # helper function to draw points of computer car's path
    # def draw_points(self, window: pygame.display) -> None:
    #     for point in self.path:
    #         pygame.draw.circle(window, (255, 0, 0), point, 2)

    # def calculate_angle(self) -> None:
    #     target_x, target_y = self.path[self.current_point]
    #     x_diff = target_x - self.x
    #     y_diff = target_y - self.y
    #
    #     if y_diff == 0:
    #         desired_radian_angle = math.pi / 2
    #     else:
    #         desired_radian_angle = math.atan(x_diff / y_diff)
    #
    #     if target_y > self.y:
    #         desired_radian_angle += math.pi
    #
    #     difference_in_angle = self.angle - math.degrees(desired_radian_angle)
    #
    #     if difference_in_angle >= 180:
    #         difference_in_angle -= 360
    #
    #     if difference_in_angle > 0:
    #         self.angle -= min(self.rotation_vel, abs(difference_in_angle))
    #     else:
    #         self.angle += min(self.rotation_vel, abs(difference_in_angle))
    #
    # def update_path_point(self) -> None:
    #     target = self.path[self.current_point]
    #     rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
    #
    #     if rect.center == target:
    #         # time.sleep(0.2)
    #         self.current_point += 1

    # def move(self) -> None:
    #     if self.current_point >= len(self.path):
    #         return
    #
    #     self.calculate_angle()
    #     self.update_path_point()
    #     super().move()