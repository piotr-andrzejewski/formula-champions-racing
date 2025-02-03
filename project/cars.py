# definition of cars

import math
import numpy

import pygame.transform
from scipy.interpolate import CubicSpline
from pygame.mask import Mask
from pygame.surface import Surface

from images import CAR_1, CAR_2, CAR_3, CAR_4, CAR_5, CAR_6, CAR_7, CAR_8
from utils import blit_rotate_center, draw_points

# constants
TRACK_POSITIONS = {
    'TRACK 1 P1': (380.0, 772),
    'TRACK 1 P2': (400.0, 758.5),
    'TRACK 1 P3': (420.0, 772),
    'TRACK 1 P4': (440.0, 758.5),
    'TRACK 1 P5': (460.0, 772),
    'TRACK 1 P6': (480.0, 758.5),
    'TRACK 1 P7': (500.0, 772),
    'TRACK 1 P8': (520.0, 758.5),
    'TRACK 2 P1': (380.0, 772),
    'TRACK 2 P2': (400.0, 758.5),
    'TRACK 2 P3': (420.0, 772),
    'TRACK 2 P4': (440.0, 758.5),
    'TRACK 2 P5': (460.0, 772),
    'TRACK 2 P6': (480.0, 758.5),
    'TRACK 2 P7': (500.0, 772),
    'TRACK 2 P8': (520.0, 758.5),
    'TRACK 3 P1': (380.0, 772),
    'TRACK 3 P2': (400.0, 758.5),
    'TRACK 3 P3': (420.0, 772),
    'TRACK 3 P4': (440.0, 758.5),
    'TRACK 3 P5': (460.0, 772),
    'TRACK 3 P6': (480.0, 758.5),
    'TRACK 3 P7': (500.0, 772),
    'TRACK 3 P8': (520.0, 758.5),
}
RESET_POSITIONS = {
    'TRACK 1': (528.5, 758.5),
    'TRACK 2': (528.5, 758.5),
    'TRACK 3': (528.5, 758.5),
}
PATHS = {
    'TRACK 1': [
        (234, 774), (71, 773), (26, 744), (96, 686), (200, 670),
        (332, 668), (377, 642), (363, 598), (286, 557), (241, 405),
        (211, 250), (169, 168), (74, 98), (105, 30), (182, 16),
        (290, 32), (328, 75), (416, 150), (492, 126), (554, 128),
        (598, 189), (658, 251), (751, 290), (774, 366), (766, 526),
        (759, 597), (730, 621), (650, 608), (582, 610), (550, 647),
        (622, 675), (694, 672), (746, 705), (723, 767), (624, 778),
        (455, 773)
    ],
    'TRACK 2': [
        (234, 774), (71, 773), (26, 744), (96, 686), (200, 670),
        (332, 668), (377, 642), (363, 598), (286, 557), (241, 405),
        (211, 250), (169, 168), (74, 98), (105, 30), (182, 16),
        (290, 32), (328, 75), (416, 150), (492, 126), (554, 128),
        (598, 189), (658, 251), (751, 290), (774, 366), (766, 526),
        (759, 597), (730, 621), (650, 608), (582, 610), (550, 647),
        (622, 675), (694, 672), (746, 705), (723, 767), (624, 778),
        (455, 773)
    ],
    'TRACK 3': [
        (234, 774), (71, 773), (26, 744), (96, 686), (200, 670),
        (332, 668), (377, 642), (363, 598), (286, 557), (241, 405),
        (211, 250), (169, 168), (74, 98), (105, 30), (182, 16),
        (290, 32), (328, 75), (416, 150), (492, 126), (554, 128),
        (598, 189), (658, 251), (751, 290), (774, 366), (766, 526),
        (759, 597), (730, 621), (650, 608), (582, 610), (550, 647),
        (622, 675), (694, 672), (746, 705), (723, 767), (624, 778),
        (455, 773)
    ]
}
POINT_MARGIN = 20.0
COLLISION_POINTS = {
    'TRACK 1': [
        (70, 745), (350, 630), (110, 80), (520, 150),
        (735, 330), (725, 590), (595, 640), (700, 720)
    ],
    'TRACK 2': [
        (70, 745), (350, 630), (110, 80), (520, 150),
        (735, 330), (725, 590), (595, 640), (700, 720)
    ],
    'TRACK 3': [
        (70, 745), (350, 630), (110, 80), (520, 150),
        (735, 330), (725, 590), (595, 640), (700, 720)
    ]
}

class BaseCar:
    IMG = CAR_1
    START_POS = TRACK_POSITIONS['TRACK 1 P1']
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
        return 1.0
    elif img == CAR_4:
        return 0.93
    elif img == CAR_5:
        return 0.98
    elif img == CAR_6:
        return 0.9
    elif img == CAR_7:
        return 0.91
    else:
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
        self.out_of_track = False

        if self.lap_times is None:
            self.lap_times = []

    def reset(self) -> None:
        self.score = 0
        self.final_position = 1
        self.lap_start_time = 0.0
        self.lap_times = []
        self.best_lap = None
        self.out_of_track = False
        super().reset()

    def brake(self) -> None:
        self.vel = max(self.vel - self.acceleration, 0)
        self.move()

    def reduce_speed(self) -> None:
        self.vel = max(self.vel - self.acceleration / 3, 0)
        self.move()

    def reset_position(self) -> None:
        self.x_pos, self.y_pos = RESET_POSITIONS['TRACK 1']
        self.angle = 90.0
        self.vel = 0.0

    def corner_cut(self, points: list[tuple[int, int]]) -> bool:
        for point in points:
            if math.hypot(point[0] - self.x_pos, point[1] - self.y_pos) < POINT_MARGIN:
                return True

        return False

    def find_best_lap(self) -> None:
        lap_times_length = len(self.lap_times)

        if lap_times_length == 0:
            return

        self.best_lap = (1, self.lap_times[0])

        for i in range(lap_times_length - 1):
            if self.lap_times[i + 1] < self.lap_times[i]:
                self.best_lap = (i + 2, self.lap_times[i + 1])


class ComputerCar(BaseCar):
    LEVEL = 1

    def __init__(
            self,
            img: Surface = BaseCar.IMG,
            level: int = LEVEL,
            start_pos: tuple[int, int] = TRACK_POSITIONS['TRACK 1 P2']
    ) -> None:
        super().__init__()

        self.path = PATHS['TRACK 1']
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
            if math.hypot(target_x - self.x_pos, target_y - self.y_pos) < POINT_MARGIN:
                self.current_point += 1

    # function to interpolate path with cubic splines to make more smooth path to follow
    def smooth_path(self) -> list[tuple[int, int]]:

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

        # function to draw path points
        draw_points(self.path, window)