# menus

import sys
import pygame
import random

from pygame import Surface

from game import Game
from settings import CARS, TRACKS, LAPS, OPPONENTS, OPPONENTS_LEVEL, STARTING_POSITIONS, CAR_NAMES, TRACK_NAMES, \
    PENALTIES, Settings
from utils import MAIN_FONT_SIZE, SECONDARY_FONT_SIZE, SELECTION_FONT_SIZE, TITLE_FONT_SIZE, \
    blit_screen, create_text, get_font, Button

# instantiate Settings class
settings = Settings()


class Menu:
    def __init__(self, game_window: Surface) -> None:
        self.game_window = game_window
        self.display_main_menu = True
        self.play_game = False
        self.set_options = False

    def main_menu(self) -> None:
        while self.display_main_menu:
            self.game_window.fill('black')
            mouse_pos = pygame.mouse.get_pos()

            self.create_main_menu_texts()

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

                    if buttons['settings'].check_for_input(mouse_pos):
                        self.set_options = True
                        self.display_main_menu = False
                        self.settings_menu()

                    if buttons['quit'].check_for_input(mouse_pos):
                        self.quit_game()

            pygame.display.update()

    def create_main_menu_texts(self) -> None:
        create_text(self.game_window, TITLE_FONT_SIZE, 'MAIN MENU', '#b68f40', (400, 200))

    def run_game(self) -> None:
        self.play_game = True
        self.display_main_menu = False
        self.check_if_random_position()
        game = Game(self.game_window, settings)
        game.run()
        self.back_to_main_menu()

    def settings_menu(self) -> None:
        self.set_options = True
        self.display_main_menu = False

        while self.set_options:
            self.game_window.fill('black')
            mouse_pos = pygame.mouse.get_pos()
            # print(mouse_pos)

            self.create_settings_texts()

            buttons = self.create_settings_buttons()

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
        self.display_main_menu = True
        self.main_menu()

    def create_settings_texts(self) -> None:
        left_pos = 450
        right_pos = 600
        top_pos = 250
        interval = 50

        create_text(
            self.game_window,
            TITLE_FONT_SIZE,
            'SETTINGS',
            '#b68f40',
            (400, 100)
        )
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
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            settings.selected_car_name,
            position=(right_pos, top_pos + interval)
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'TRACK',
            position=(left_pos, top_pos + interval * 2),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            settings.selected_track_name,
            position=(right_pos, top_pos + interval * 2)
        )
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
        return {
            'play': Button(
                position=(400, 400),
                text_input='PLAY',
                font=get_font(MAIN_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'settings': Button(
                position=(400, 500),
                text_input='SETTINGS',
                font=get_font(MAIN_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'quit': Button(
                position=(400, 600),
                text_input='QUIT',
                font=get_font(MAIN_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            )
        }

    @staticmethod
    def create_settings_buttons() -> dict[str, Button]:
        left_pos = 500
        right_pos = 700
        top_pos = 300
        interval = 50

        return {
            'select_car_previous': Button(
                position=(left_pos, top_pos),
                text_input='<',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_car_next': Button(
                position=(right_pos, top_pos),
                text_input='>',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_track_previous': Button(
                position=(left_pos, top_pos + interval),
                text_input='<',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_track_next': Button(
                position=(right_pos, top_pos + interval),
                text_input='>',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_laps_previous': Button(
                position=(left_pos, top_pos + interval * 2),
                text_input='<',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_laps_next': Button(
                position=(right_pos, top_pos + interval * 2),
                text_input='>',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_opponents_previous': Button(
                position=(left_pos, top_pos + interval * 3),
                text_input='<',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_opponents_next': Button(
                position=(right_pos, top_pos + interval * 3),
                text_input='>',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_opponents_level_previous': Button(
                position=(left_pos, top_pos + interval * 4),
                text_input='<',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_opponents_level_next': Button(
                position=(right_pos, top_pos + interval * 4),
                text_input='>',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_starting_position_previous': Button(
                position=(left_pos, top_pos + interval * 5),
                text_input='<',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_starting_position_next': Button(
                position=(right_pos, top_pos + interval * 5),
                text_input='>',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_penalties_previous': Button(
                position=(left_pos, top_pos + interval * 6),
                text_input='<',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'select_penalties_next': Button(
                position=(right_pos, top_pos + interval * 6),
                text_input='>',
                font=get_font(SELECTION_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            ),
            'back': Button(
                position=(125, 700),
                text_input='BACK',
                font=get_font(SECONDARY_FONT_SIZE),
                base_color='#d7fcd4',
                hover_color='white'
            )
        }

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

