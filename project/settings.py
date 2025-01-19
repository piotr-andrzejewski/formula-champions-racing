# game settings
import random

from pygame import Surface

from cars import TRACK_POSITIONS
from images import CAR_1, CAR_2, CAR_3, CAR_4, CAR_5, CAR_6, CAR_7, CAR_8, TRACK_1, TRACK_2, TRACK_3

# options for player to choose from
CARS = [CAR_1, CAR_2, CAR_3, CAR_4, CAR_5, CAR_6, CAR_7, CAR_8]
CAR_NAMES = ['CAR 1', 'CAR 2', 'CAR 3', 'CAR 4', 'CAR 5', 'CAR 6', 'CAR 7', 'CAR 8']
TRACKS = [TRACK_1, TRACK_2, TRACK_3]
TRACK_NAMES = ['TRACK 1', 'TRACK 2', 'TRACK 3']
LAPS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
OPPONENTS = [0, 1, 2, 3, 4, 5, 6, 7]
OPPONENTS_LEVEL = [1, 2, 3]
STARTING_POSITIONS = [1, 2, 3, 4, 5, 6, 7, 8, 'RANDOM']


def create_track_position_name(track_name: str, position: int) -> str:
    track_position_name = track_name.replace(' ', '_') + '_' + str(position)

    return track_position_name


def remove_random_from_starting_positions(starting_positions: list[int | str]) -> list[int]:
    starting_positions.remove('RANDOM')

    return starting_positions


def get_available_starting_positions(
        starting_positions: list[int | str],
        occupied_positions: list[int] = None
) -> list[int]:
    if occupied_positions is None:
        occupied_positions = []

    available_starting_positions = starting_positions.copy()

    for occupied_position in occupied_positions:
        available_starting_positions.remove(occupied_position)

    return remove_random_from_starting_positions(available_starting_positions)


def get_opponent_starting_position(
        occupied_starting_positions: list[int]
) -> int:
    available_starting_positions = get_available_starting_positions(STARTING_POSITIONS, occupied_starting_positions)
    position = random.randint(available_starting_positions[0], available_starting_positions[-1])

    while position in occupied_starting_positions:
        position = random.randint(available_starting_positions[0], available_starting_positions[-1])

    return position


def get_opponent_car(occupied_cars: list[Surface]) -> Surface:
    available_cars = CARS.copy()

    for car in occupied_cars:
        available_cars.remove(car)

    return available_cars[0]


def get_random_starting_position() -> int:
    return random.randint(STARTING_POSITIONS[0], STARTING_POSITIONS[-2])


class Settings:
    def __init__(
            self,
            player_nickname: str = 'PLAYER 1',
            car: Surface = CARS[0],
            car_name: str = CAR_NAMES[0],
            track: Surface = TRACKS[0],
            track_name: str = TRACK_NAMES[0],
            laps: int = LAPS[0],
            opponents: int = OPPONENTS[0],
            opponents_level: int = OPPONENTS_LEVEL[0],
            start_pos: int = STARTING_POSITIONS[0]
    ) -> None:

        if player_nickname == '':
            self.player_nickname = 'PLAYER 1'

        self.player_nickname = player_nickname
        self.selected_car = car
        self.selected_car_name = car_name
        self.selected_track = track
        self.selected_track_name = track_name
        self.selected_laps = laps
        self.opponents = opponents
        self.opponents_level = opponents_level
        self.starting_position = start_pos
        self.selected_starting_position = self.starting_position
        self.occupied_starting_positions = []

    def reset(self) -> None:
        self.selected_car = CARS[0]
        self.selected_car_name = CAR_NAMES[0]
        self.selected_track = TRACKS[0]
        self.selected_track_name = TRACK_NAMES[0]
        self.selected_laps = LAPS[0]
        self.opponents = OPPONENTS[0]
        self.opponents_level = OPPONENTS_LEVEL[0]
        self.starting_position = STARTING_POSITIONS[0]
        self.selected_starting_position = self.starting_position
        self.occupied_starting_positions = []

    def get_player_starting_track_position(self) -> tuple[float, float]:
        starting_position = self.selected_starting_position

        if starting_position == 'RANDOM':
            starting_position = get_random_starting_position()
            self.starting_position = starting_position

        self.occupied_starting_positions.append(self.starting_position)

        return TRACK_POSITIONS[create_track_position_name(self.selected_track_name, self.starting_position)]

    def get_opponent_starting_track_position(self) -> tuple[float, float]:
        opponent_starting_position = get_opponent_starting_position(self.occupied_starting_positions)
        self.occupied_starting_positions.append(opponent_starting_position)

        return TRACK_POSITIONS[create_track_position_name(self.selected_track_name, opponent_starting_position)]