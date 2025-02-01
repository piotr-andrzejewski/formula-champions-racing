# menus

import sys

import pygame.constants
from pygame import Surface

from game import Game
from images import CUP
from settings import *
from utils import *

# instantiate Settings class
settings = Settings()


class Menu:
    def __init__(self, game_window: Surface) -> None:
        self.game_window = game_window
        self.display_main_menu = True
        self.play_game = False
        self.set_options = False
        self.show_highscores = False

    def main_menu(self) -> None:
        while self.display_main_menu:
            self.game_window.fill('black')
            self.create_header(
                font_size=MAIN_FONT_SIZE,
                text='FORMULA',
                position=(500, 125),
            )
            self.create_header(
                font_size=MAIN_FONT_SIZE,
                text='CHAMPIONS',
                position=(500, 200),
            )
            self.create_header(
                font_size=MAIN_FONT_SIZE,
                text='RACING',
                position=(500, 275),
            )
            self.game_window.blit(scale_image(CUP, 2), (50, 90))

            mouse_pos = pygame.mouse.get_pos()
            buttons = self.create_main_menu_buttons()

            for button in buttons.values():
                button.change_color(mouse_pos)
                button.update(self.game_window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons['play'].check_for_input(mouse_pos):
                        blit_screen(self.game_window)
                        self.run_game()

                    if buttons['highscores'].check_for_input(mouse_pos):
                        self.show_highscores = True
                        self.display_main_menu = False
                        self.highscores_menu()

                    if buttons['settings'].check_for_input(mouse_pos):
                        self.set_options = True
                        self.display_main_menu = False
                        self.settings_menu()

                    if buttons['quit'].check_for_input(mouse_pos):
                        self.quit_game()

            pygame.display.update()

    def create_header(
            self,
            font_size: int = TITLE_FONT_SIZE,
            text: str = 'HEADER',
            color: str = '#b68f40',
            position: tuple[int, int] = (400, 100),
            positioning: str = 'center'
    ) -> None:
        create_text(
            self.game_window,
            font_size,
            text,
            color,
            position,
            positioning
        )

    def run_game(self) -> None:
        self.play_game = True
        self.display_main_menu = False
        self.check_if_random_position()
        game = Game(self.game_window, settings)
        game.run()
        self.back_to_main_menu()

    def highscores_menu(self) -> None:
        self.show_highscores = True
        self.display_main_menu = False
        filename = 'highscores.csv'
        highscores = read_highscores_file(filename)

        while self.show_highscores:
            self.game_window.fill('black')
            mouse_pos = pygame.mouse.get_pos()

            self.create_header(font_size=MAIN_FONT_SIZE, text='HIGHSCORES', position=(400, 100))
            self.create_highscores_labels()

            for i in range(len(highscores)):
                self.create_highscores_row(highscores[i], i + 1)

            back_button = self.create_back_button()
            back_button.change_color(mouse_pos)
            back_button.update(self.game_window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN and event.key == pygame.constants.K_ESCAPE:
                    self.back_to_main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.check_for_input(mouse_pos):
                        self.back_to_main_menu()

            pygame.display.update()

    def settings_menu(self) -> None:
        self.set_options = True
        self.display_main_menu = False

        while self.set_options:
            self.game_window.fill('black')
            mouse_pos = pygame.mouse.get_pos()
            # print(mouse_pos)
            self.create_header(font_size=MAIN_FONT_SIZE, text='SETTINGS', position=(400, 100))
            self.create_settings_items()

            buttons = self.create_settings_buttons()
            buttons['back'] = self.create_back_button()

            for button in buttons.values():
                button.change_color(mouse_pos)
                button.update(self.game_window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        self.back_to_main_menu()

                    # check for backspace
                    if event.key == pygame.K_BACKSPACE:

                        # get text input from 0 to -1 i.e. end.
                        settings.player_nickname = settings.player_nickname[:-1]

                    # Unicode standard is used for string formation
                    else:
                        if len(settings.player_nickname) < 10:
                            settings.player_nickname += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons['select_car_previous'].check_for_input(mouse_pos):
                        index_of_current_car = CARS.index(settings.selected_car)

                        if index_of_current_car > 0:
                            settings.selected_car = CARS[index_of_current_car - 1]
                            settings.selected_car_name = CAR_NAMES[index_of_current_car - 1]

                    if buttons['select_car_next'].check_for_input(mouse_pos):
                        index_of_current_car = CARS.index(settings.selected_car)

                        if index_of_current_car < len(CARS) - 1:
                            settings.selected_car = CARS[index_of_current_car + 1]
                            settings.selected_car_name = CAR_NAMES[index_of_current_car + 1]

                    if buttons['select_track_previous'].check_for_input(mouse_pos):
                        index_of_current_track = TRACKS.index(settings.selected_track)

                        if index_of_current_track > 0:
                            settings.selected_track = TRACKS[index_of_current_track - 1]
                            settings.selected_track_name = TRACK_NAMES[index_of_current_track - 1]

                    if buttons['select_track_next'].check_for_input(mouse_pos):
                        index_of_current_track = TRACKS.index(settings.selected_track)

                        if index_of_current_track < len(TRACKS) - 1:
                            settings.selected_track = TRACKS[index_of_current_track + 1]
                            settings.selected_track_name = TRACK_NAMES[index_of_current_track + 1]

                    if buttons['select_laps_previous'].check_for_input(mouse_pos):
                        index_of_current_lap = LAPS.index(settings.selected_laps)

                        if index_of_current_lap > 0:
                            settings.selected_laps = LAPS[index_of_current_lap - 1]

                    if buttons['select_laps_next'].check_for_input(mouse_pos):
                        index_of_current_lap = LAPS.index(settings.selected_laps)

                        if index_of_current_lap < len(LAPS) - 1:
                            settings.selected_laps = LAPS[index_of_current_lap + 1]

                    if buttons['select_opponents_previous'].check_for_input(mouse_pos):
                        index_of_current_opponents = OPPONENTS.index(settings.opponents)

                        if index_of_current_opponents > 0:
                            settings.opponents = OPPONENTS[index_of_current_opponents - 1]

                    if buttons['select_opponents_next'].check_for_input(mouse_pos):
                        index_of_current_opponents = OPPONENTS.index(settings.opponents)

                        if index_of_current_opponents < len(OPPONENTS) - 1:
                            settings.opponents = OPPONENTS[index_of_current_opponents + 1]

                    if buttons['select_opponents_level_previous'].check_for_input(mouse_pos):
                        index_of_current_opponents_level = OPPONENTS_LEVEL.index(settings.opponents_level)

                        if index_of_current_opponents_level > 0:
                            settings.opponents_level = OPPONENTS_LEVEL[index_of_current_opponents_level - 1]

                    if buttons['select_opponents_level_next'].check_for_input(mouse_pos):
                        index_of_current_opponents_level = OPPONENTS_LEVEL.index(settings.opponents_level)

                        if index_of_current_opponents_level < len(OPPONENTS_LEVEL) - 1:
                            settings.opponents_level = OPPONENTS_LEVEL[index_of_current_opponents_level + 1]

                    if buttons['select_starting_position_previous'].check_for_input(mouse_pos):
                        index_of_current_starting_position = STARTING_POSITIONS.index(settings.starting_position)

                        if index_of_current_starting_position > 0:
                            settings.starting_position = STARTING_POSITIONS[index_of_current_starting_position - 1]
                            settings.selected_starting_position = STARTING_POSITIONS[index_of_current_starting_position - 1]

                    if buttons['select_starting_position_next'].check_for_input(mouse_pos):
                        index_of_current_starting_position = STARTING_POSITIONS.index(settings.starting_position)

                        if index_of_current_starting_position < len(STARTING_POSITIONS) - 1:
                            settings.starting_position = STARTING_POSITIONS[index_of_current_starting_position + 1]
                            settings.selected_starting_position = STARTING_POSITIONS[index_of_current_starting_position + 1]

                    if buttons['select_penalties_previous'].check_for_input(mouse_pos):
                        index_of_current_penalties = PENALTIES.index(settings.penalties)

                        if index_of_current_penalties > 0:
                            settings.penalties = PENALTIES[index_of_current_penalties - 1]

                    if buttons['select_penalties_next'].check_for_input(mouse_pos):
                        index_of_current_penalties = PENALTIES.index(settings.penalties)

                        if index_of_current_penalties < len(PENALTIES) - 1:
                            settings.penalties = PENALTIES[index_of_current_penalties + 1]

                    if buttons['back'].check_for_input(mouse_pos):
                        self.back_to_main_menu()

            pygame.display.update()

    def back_to_main_menu(self) -> None:
        self.play_game = False
        self.set_options = False
        self.show_highscores = False
        self.display_main_menu = True
        self.main_menu()

    def create_highscores_labels(self) -> None:
        left_pos = 40
        top_pos = 200
        interval = 100

        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'PLACE',
            position=(left_pos, top_pos),
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'SCORE',
            position=(left_pos + interval, top_pos),
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'NICKNAME',
            position=(left_pos + interval * 2 + 30, top_pos),
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'CAR',
            position=(left_pos + interval * 3 + 50, top_pos)
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'TRACK',
            position=(left_pos + interval * 4 + 60, top_pos)
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'BEST LAP',
            position=(left_pos + interval * 5 + 90, top_pos)
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'PENALTIES',
            position=(left_pos + interval * 6 + 100, top_pos)
        )

    def create_highscores_row(self, data: list[int | str], row_number: int) -> None:
        left_pos = 40
        top_pos = 200 + 50 * row_number
        interval = 100

        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(data[0]),
            position=(left_pos, top_pos),
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(data[1]),
            position=(left_pos + interval, top_pos),
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(data[2]),
            position=(left_pos + interval * 2 + 30, top_pos),
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(data[3]),
            position=(left_pos + interval * 3 + 50, top_pos)
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(data[4]),
            position=(left_pos + interval * 4 + 60, top_pos)
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(data[5]),
            position=(left_pos + interval * 5 + 90, top_pos)
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(data[6]),
            position=(left_pos + interval * 6 + 100, top_pos)
        )

    def create_settings_items(self) -> None:
        left_pos = 450
        right_pos = 600
        top_pos = 250
        interval = 50

        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'NICKNAME',
            position=(left_pos, top_pos),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            settings.player_nickname,
            position=(right_pos, top_pos)
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'CAR',
            position=(left_pos, top_pos + interval),
            positioning='midright'
        )
        self.game_window.blit(pygame.transform.rotate(scale_image(settings.selected_car, 2), 90), (585, 295))
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'TRACK',
            position=(left_pos, top_pos + interval * 2),
            positioning='midright'
        )
        self.game_window.blit(scale_image(settings.selected_track, 0.08), (565, 320))
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'LAPS',
            position=(left_pos, top_pos + interval * 3),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(settings.selected_laps),
            position=(right_pos, top_pos + interval * 3)
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'OPPONENTS',
            position=(left_pos, top_pos + interval * 4),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(settings.opponents),
            position=(right_pos, top_pos + interval * 4)
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'OPPONENTS LEVEL',
            position=(left_pos, top_pos + interval * 5),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(settings.opponents_level),
            position=(right_pos, top_pos + interval * 5)
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'STARTING POSITION',
            position=(left_pos, top_pos + interval * 6),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(settings.selected_starting_position),
            position=(right_pos, top_pos + interval * 6)
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'PENALTIES',
            position=(left_pos, top_pos + interval * 7),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(settings.penalties),
            position=(right_pos, top_pos + interval * 7)
        )

    @staticmethod
    def create_main_menu_buttons() -> dict[str, Button]:
        x_pos = 400
        y_pox_top = 425
        interval = 80

        return {
            'play': create_button(
                position=(x_pos, y_pox_top),
                text='PLAY',
                font_size=SECONDARY_FONT_SIZE
            ),
            'settings': create_button(
                position=(x_pos, y_pox_top + interval),
                text='SETTINGS',
                font_size=SECONDARY_FONT_SIZE
            ),
            'highscores': create_button(
                position=(x_pos, y_pox_top + interval * 2),
                text='HIGHSCORES',
                font_size=SECONDARY_FONT_SIZE
            ),
            'quit': create_button(
                position=(x_pos, y_pox_top + interval * 3),
                text='QUIT',
                font_size=SECONDARY_FONT_SIZE
            )
        }

    @staticmethod
    def create_settings_buttons() -> dict[str, Button]:
        left_pos = 500
        right_pos = 700
        top_pos = 300
        interval = 50

        return {
            'select_car_previous': create_button(
                position=(left_pos, top_pos),
                text='<',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_car_next': create_button(
                position=(right_pos, top_pos),
                text='>',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_track_previous': create_button(
                position=(left_pos, top_pos + interval),
                text='<',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_track_next': create_button(
                position=(right_pos, top_pos + interval),
                text='>',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_laps_previous': create_button(
                position=(left_pos, top_pos + interval * 2),
                text='<',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_laps_next': create_button(
                position=(right_pos, top_pos + interval * 2),
                text='>',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_opponents_previous': create_button(
                position=(left_pos, top_pos + interval * 3),
                text='<',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_opponents_next': create_button(
                position=(right_pos, top_pos + interval * 3),
                text='>',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_opponents_level_previous': create_button(
                position=(left_pos, top_pos + interval * 4),
                text='<',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_opponents_level_next': create_button(
                position=(right_pos, top_pos + interval * 4),
                text='>',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_starting_position_previous': create_button(
                position=(left_pos, top_pos + interval * 5),
                text='<',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_starting_position_next': create_button(
                position=(right_pos, top_pos + interval * 5),
                text='>',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_penalties_previous': create_button(
                position=(left_pos, top_pos + interval * 6),
                text='<',
                font_size=SELECTION_FONT_SIZE
            ),
            'select_penalties_next': create_button(
                position=(right_pos, top_pos + interval * 6),
                text='>',
                font_size=SELECTION_FONT_SIZE
            )
        }

    @staticmethod
    def create_back_button(
            position: tuple[int, int] = (125, 700),
            font_size: int = SECONDARY_FONT_SIZE
    ) -> Button:
        return create_button(
            position=position,
            text='BACK',
            font_size=font_size
        )

    @staticmethod
    def quit_game() -> None:
        pygame.quit()
        sys.exit()

    @staticmethod
    def generate_random_position() -> int:
        return random.randint(1, 8)

    @staticmethod
    def check_if_random_position() -> None:
        if settings.starting_position == 'RANDOM':
            settings.starting_position = Menu.generate_random_position()

