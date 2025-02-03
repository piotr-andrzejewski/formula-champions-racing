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
    'TRACK 1 P1': (484.0, 743.0),
    'TRACK 1 P2': (501.0, 729.5),
    'TRACK 1 P3': (520.0, 743.0),
    'TRACK 1 P4': (537.0, 729.5),
    'TRACK 1 P5': (556.0, 743.0),
    'TRACK 1 P6': (573.0, 729.5),
    'TRACK 1 P7': (592.0, 743.0),
    'TRACK 1 P8': (609.0, 729.5),
    'TRACK 2 P1': (647.0, 592.0),
    'TRACK 2 P2': (658.0, 580.0),
    'TRACK 2 P3': (671.0, 592.0),
    'TRACK 2 P4': (682.0, 580.0),
    'TRACK 2 P5': (695.0, 592),
    'TRACK 2 P6': (707.0, 580.0),
    'TRACK 2 P7': (719.0, 592),
    'TRACK 2 P8': (731.0, 580.0),
    'TRACK 3 P1': (417.5, 230.0),
    'TRACK 3 P2': (429.5, 244.0),
    'TRACK 3 P3': (441.5, 230.0),
    'TRACK 3 P4': (453.5, 244.0),
    'TRACK 3 P5': (465.5, 230.0),
    'TRACK 3 P6': (477.5, 244.0),
    'TRACK 3 P7': (489.5, 230.0),
    'TRACK 3 P8': (501.5, 244.0),
}
RESET_POSITIONS = {
    'TRACK 1': (628.5, 729.5),
    'TRACK 2': (748.0, 580.0),
    'TRACK 3': (388.0, 244.0),
}
PATHS = {
    'TRACK 1': [
        (231, 750),
        (151, 711),
        (246, 646),
        (422, 653),
        (485, 596),
        (386, 540),
        (340, 321),
        (283, 189),
        (194, 106),
        (271, 41),
        (418, 87),
        (478, 143),
        (547, 159),
        (629, 148),
        (707, 247),
        (827, 314),
        (835, 557),
        (775, 599),
        (673, 582),
        (666, 646),
        (797, 655),
        (797, 731),
        (643, 749),
        (479, 748)
    ],
    'TRACK 2': [
        (513, 597),
        (389, 578),
        (312, 579),
        (178, 560),
        (113, 424),
        (81, 302),
        (32, 188),
        (69, 136),
        (169, 124),
        (273, 269),
        (375, 368),
        (465, 439),
        (615, 471),
        (903, 466),
        (949, 542),
        (833, 588),
        (637, 598)
    ],
    'TRACK 3': [
        (255, 228),
        (185, 269),
        (186, 345),
        (176, 473),
        (476, 669),
        (591, 702),
        (636, 624),
        (596, 518),
        (486, 393),
        (491, 312),
        (589, 291),
        (603, 338),
        (602, 397),
        (753, 371),
        (722, 425),
        (672, 468),
        (723, 583),
        (786, 613),
        (847, 506),
        (820, 379),
        (669, 274),
        (491, 238),
        (361, 230)
    ]
}
POINT_MARGIN = 20.0
COLLISION_POINTS = {
    'TRACK 1': [
        (170, 745),
        (450, 630),
        (210, 80),
        (620, 150),
        (835, 330),
        (825, 590),
        (695, 640),
        (800, 720)
    ],
    'TRACK 2': [
        (64, 164),
        (148, 141),
        (928, 509)
    ],
    'TRACK 3': [
        (218, 274),
        (165, 310),
        (190, 431),
        (582, 672),
        (509, 347),
        (574, 322),
        (624, 367),
        (698, 396),
        (701, 476),
        (779, 577)
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
        self.crossed_finish_line = False
        self.crossed_start_line = False

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
        self.crossed_finish_line = False
        self.crossed_start_line = False


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
    elif img == CAR_8:
        return 0.93
    else:
        return 0.9


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

    def reset_position(self, track_name: str) -> None:
        self.x_pos, self.y_pos = RESET_POSITIONS[track_name]
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
            start_pos: tuple[float, float] = TRACK_POSITIONS['TRACK 1 P2'],
            path: list[tuple[int, int]] = None,
            track_name: str = 'TRACK 1'
    ) -> None:
        super().__init__()

        if path is None:
            path = PATHS[track_name]

        self.path = path
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