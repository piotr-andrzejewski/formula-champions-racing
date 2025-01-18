# definition of cars

import pygame
import math
import numpy

from scipy.interpolate import CubicSpline
from pygame import Mask, Surface

from images import CAR_1, CAR_2, CAR_3, CAR_4, CAR_5, CAR_6, CAR_7, CAR_8
from utils import blit_rotate_center

# constants
TRACK_1_P1 = (380.0, 772)
TRACK_1_P2 = (400.0, 758.5)
TRACK_1_P3 = (420.0, 772)
TRACK_1_P4 = (440.0, 758.5)
TRACK_1_P5 = (460.0, 772)
TRACK_1_P6 = (480.0, 758.5)
TRACK_1_P7 = (500.0, 772)
TRACK_1_P8 = (520.0, 758.5)
TRACK_1_RESET_POSITION = (528.5, 758.5)
TRACK_1_PATH = [
    (234.0, 774.0), (71.0, 773.0), (26.0, 744.0), (96.0, 686.0), (200.0, 670.0),
    (332.0, 668.0), (377.0, 642.0), (363.0, 598.0), (286.0, 557.0), (241.0, 405.0),
    (211.0, 250.0), (169.0, 168.0), (74.0, 98.0), (105.0, 30.0), (182.0, 16.0), (290.0, 32.0),
    (328.0, 75.0), (416.0, 150.0), (492.0, 126.0), (554.0, 128.0), (598.0, 189.0),
    (658.0, 251.0), (751.0, 290.0), (774.0, 366.0), (766.0, 526.0), (759.0, 597.0),
    (730.0, 621.0), (650.0, 608.0), (582.0, 610.0), (550.0, 647.0), (622.0, 675.0),
    (694.0, 672.0), (746.0, 705.0), (723.0, 767.0), (624.0, 778.0), (455.0, 773.0)
]
TRACK_1_PATH_POINT_MARGIN = 20.0


class BaseCar:
    IMG = CAR_1
    START_POS = TRACK_1_P1
    MAX_VEL = 3.0

    def __init__(self) -> None:
        self.img = self.IMG
        self.max_vel = self.MAX_VEL
        self.vel = 0.0
        self.angle = 90.0
        self.x_pos, self.y_pos = self.START_POS
        self.acceleration = 0.1
        self.completed_laps = 0
        self.crossed_line = False

    def rotate(self, left=False, right=False) -> None:
        if left:
            self.angle += self.max_vel
        elif right:
            self.angle -= self.max_vel

    def draw(self, window: Surface) -> None:
        blit_rotate_center(window, self.img, (self.x_pos, self.y_pos), self.angle)

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

        self.y_pos -= vertical
        self.x_pos -= horizontal

    def collide(self, mask: Mask, x=0.0, y=0.0) -> tuple[float, float] | None:
        car_mask = pygame.mask.from_surface(self.img)
        offset = (float(self.x_pos - x), float(self.y_pos - y))
        poi = mask.overlap(car_mask, offset)

        return poi

    def reset(self) -> None:
        self.x_pos, self.y_pos = self.START_POS
        self.angle = 90.0
        self.vel = 0.0
        self.completed_laps = 0
        self.crossed_line = False


def calculate_vel_factor(img: Surface) -> float:
    if img == CAR_1:
        return 0.96
    elif img == CAR_2:
        return 0.96
    elif img == CAR_3:
        return 1
    elif img == CAR_4:
        return 0.93
    elif img == CAR_5:
        return 0.98
    elif img == CAR_6:
        return 0.9
    elif img == CAR_7:
        return 0.91
    elif img == CAR_8:
        return 0.93


class PlayerCar(BaseCar):
    def __init__(
            self,
            img: Surface = BaseCar.IMG,
            start_pos: tuple[float, float] = BaseCar.START_POS
    ) -> None:
        super().__init__()
        self.img = img
        self.x_pos, self.y_pos = start_pos
        self.max_vel *= calculate_vel_factor(self.img)
        self.score = 0
        self.final_position = 1
        self.lap_start_time = 0.0
        self.lap_times = None
        self.best_lap = None

        if self.lap_times is None:
            self.lap_times = []


    def brake(self) -> None:
        self.vel = max(self.vel - self.acceleration, 0)
        self.move()

    def reduce_speed(self) -> None:
        self.vel = max(self.vel - self.acceleration / 3, 0)
        self.move()

    def reset_position(self) -> None:
        self.x_pos, self.y_pos = TRACK_1_RESET_POSITION
        self.angle = 90.0
        self.vel = 0.0

    def find_best_lap(self) -> None:
        lap_times_length = len(self.lap_times)

        if lap_times_length == 0:
            return

        self.best_lap = (1, self.lap_times[0])

        for i in range(lap_times_length - 1):
            if self.lap_times[i + 1] > self.lap_times[i]:
                self.best_lap = (i + 2, self.lap_times[i + 1])


class ComputerCar(BaseCar):
    LEVEL = 1

    def __init__(
            self,
            img: Surface = BaseCar.IMG,
            level: int = LEVEL,
            start_pos: tuple[float, float] = TRACK_1_P2
    ) -> None:
        super().__init__()

        self.path = TRACK_1_PATH
        self.current_point = 0
        self.vel = (self.MAX_VEL - 0.7 + level / 5) * calculate_vel_factor(img)
        self.img = pygame.transform.rotate(img, -90)
        self.x_pos, self.y_pos = start_pos
        self.smooth_direction = (0, 0)

    def reset(self):
        self.current_point = 0
        super().reset()

    def move_towards(self, target_x: float, target_y: float) -> None:
        # calculate the direction vector and distance
        direction = (target_x - self.x_pos, target_y - self.y_pos)
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
        self.x_pos += self.smooth_direction[0] * self.vel
        self.y_pos += self.smooth_direction[1] * self.vel

    def update_path_point(self, smooth_path: list[tuple[float, float]]) -> None:
        if self.current_point < len(smooth_path):
            target_x, target_y = smooth_path[self.current_point]
            self.move_towards(target_x, target_y)

            # checking if hypotenuse is smaller than desired margin to move to the next path point
            if math.hypot(target_x - self.x_pos, target_y - self.y_pos) < TRACK_1_PATH_POINT_MARGIN:
                self.current_point += 1

    # function to interpolate path with cubic splines to make more smooth path to follow
    def smooth_path(self) -> list[tuple[float, float]]:
        # extract x and y coordinates from points in path
        pos_x, pos_y = zip(*self.path)

        points = numpy.linspace(0, 1, len(self.path))
        cubic_spline_x = CubicSpline(points, pos_x)
        cubic_spline_y = CubicSpline(points, pos_y)
        smooth_points = numpy.linspace(0, 1, 100)

        return list(zip(cubic_spline_x(smooth_points), cubic_spline_y(smooth_points)))

    def draw(self, window: Surface) -> None:
        self.update_path_point(self.smooth_path())
        super().draw(window)

        # # use of helper function to display path points
        # self.draw_points(window)

    # helper function to draw points of computer car's path
    # def draw_points(self, window: Surface) -> None:
    #     for point in self.path:
    #         pygame.draw.circle(window, (255, 0, 0), point, 2)


def generate_player() -> PlayerCar:
    return PlayerCar(img=CAR_1, start_pos=TRACK_1_P1)


def generate_opponents() -> list[ComputerCar]:
    return [
        ComputerCar(img=CAR_2, start_pos=TRACK_1_P2),
        ComputerCar(img=CAR_3, start_pos=TRACK_1_P3),
        ComputerCar(img=CAR_4, start_pos=TRACK_1_P4),
        ComputerCar(img=CAR_5, start_pos=TRACK_1_P5),
        ComputerCar(img=CAR_6, start_pos=TRACK_1_P6),
        ComputerCar(img=CAR_7, start_pos=TRACK_1_P7),
        ComputerCar(img=CAR_8, start_pos=TRACK_1_P8)
    ]