# game settings

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
STARTING_POSITION = [1, 2, 3, 4, 5, 6, 7, 8, 'RANDOM']


def create_track_position_name(track_name: str, position: int) -> str:
    track_position_name = track_name.replace(' ', '_') + '_P' + str(position)
    track_position_name.upper()

    return track_position_name


def get_opponent_starting_position(
        occupied_track_positions: dict[str, tuple[float, float]]
) -> tuple[float, float]:
    available_track_positions = TRACK_POSITIONS

    for key in occupied_track_positions.keys():
        available_track_positions.pop(key)

    return available_track_positions[0]


def get_opponent_car(occupied_cars: list[Surface]) -> Surface:
    available_cars = CARS

    for car in occupied_cars:
        available_cars.remove(car)

    return available_cars[0]


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
            start_pos: int = STARTING_POSITION[0]
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

    def reset(self) -> None:
        self.selected_car = CARS[0]
        self.selected_car_name = CAR_NAMES[0]
        self.selected_track = TRACKS[0]
        self.selected_track_name = TRACK_NAMES[0]
        self.selected_laps = LAPS[0]
        self.opponents = OPPONENTS[0]
        self.opponents_level = OPPONENTS_LEVEL[0]
        self.starting_position = STARTING_POSITION[0]

    def get_player_starting_position(self) -> tuple[float, float]:
        track_position_name = create_track_position_name(self.selected_track_name, self.starting_position)

        return TRACK_POSITIONS[track_position_name]