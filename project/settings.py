# game settings

from pygame import Surface

from images import TRACK_1

TRACKS = [TRACK_1]
RACE_RULES = {'track_cutting': False, 'collisions': False}


class Settings:
    def __init__(
            self,
            track: Surface = TRACKS[0],
            laps: int = 1,
            opponents: int = 0,
            opponents_level: int = 1,
            start_pos: int = 1,
            race_rules = None
    ) -> None:
        if race_rules is None:
            race_rules = RACE_RULES

        self.selected_track = track
        self.selected_laps = laps
        self.opponents = opponents
        self.opponents_level = opponents_level
        self.starting_position = start_pos
        self.race_rules = race_rules

    # def get_settings(self) -> dict[str, Surface | int | int | int | int | None | dict[str, bool]]:
    #     return {
    #         'track': self.selected_track,
    #         'laps': self.selected_laps,
    #         'opponents': self.opponents,
    #         'level': self.opponents_level,
    #         'start_pos': self.starting_position,
    #         'race_rules': self.race_rules
    #     }