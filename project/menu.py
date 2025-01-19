import sys
import pygame
import random

from pygame import Surface

from game import Game
from settings import Settings, CARS, TRACKS, LAPS, OPPONENTS, OPPONENTS_LEVEL, STARTING_POSITIONS, CAR_NAMES, TRACK_NAMES
from utils import Button, blit_screen, get_font


# constants
TITLE_FONT_SIZE = 100
MAIN_FONT_SIZE = 75
SECONDARY_FONT_SIZE = 50
SELECTION_FONT_SIZE = 25


# instantiate Settings class
settings = Settings()


def create_main_menu_buttons() -> dict[str, Button]:
    return {
        'play_button': Button(
            position=(400, 400),
            text_input='PLAY',
            font=get_font(MAIN_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'settings_button': Button(
            position=(400, 500),
            text_input='SETTINGS',
            font=get_font(MAIN_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'quit_button': Button(
            position=(400, 600),
            text_input='QUIT',
            font=get_font(MAIN_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        )
    }


def create_settings_buttons() -> dict[str, Button]:
    return {
        'select_car_previous_button': Button(
            position=(500, 300),
            text_input='<',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_car_next_button': Button(
            position=(700, 300),
            text_input='>',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_track_previous_button': Button(
            position=(500, 350),
            text_input='<',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_track_next_button': Button(
            position=(700, 350),
            text_input='>',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_laps_previous_button': Button(
            position=(500, 400),
            text_input='<',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_laps_next_button': Button(
            position=(700, 400),
            text_input='>',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_opponents_previous_button': Button(
            position=(500, 450),
            text_input='<',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_opponents_next_button': Button(
            position=(700, 450),
            text_input='>',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_opponents_level_previous_button': Button(
            position=(500, 500),
            text_input='<',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_opponents_level_next_button': Button(
            position=(700, 500),
            text_input='>',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_starting_position_previous_button': Button(
            position=(500, 550),
            text_input='<',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'select_starting_position_next_button': Button(
            position=(700, 550),
            text_input='>',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        ),
        'back_button': Button(
            position=(125, 700),
            text_input='BACK',
            font=get_font(SECONDARY_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        )
    }


def quit_game() -> None:
    pygame.quit()
    sys.exit()


def generate_random_position() -> int:
    return random.randint(1, 8)


def check_if_random_position() -> None:
    if settings.starting_position == 'RANDOM':
        settings.starting_position = generate_random_position()


class Menu:
    def __init__(self, game_window: Surface) -> None:
        self.game_window = game_window
        self.display_main_menu = True
        self.play_game = False
        self.set_options = False

    def main_menu(self) -> None:
        while self.display_main_menu:
            self.game_window.fill('black')
            menu_mouse_pos = pygame.mouse.get_pos()

            self.create_main_menu_texts()

            buttons = create_main_menu_buttons()

            for button in buttons.values():
                button.change_color(menu_mouse_pos)
                button.update(self.game_window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons['play_button'].check_for_input(menu_mouse_pos):
                        blit_screen(self.game_window)
                        self.run_game()

                    if buttons['settings_button'].check_for_input(menu_mouse_pos):
                        self.set_options = True
                        self.display_main_menu = False
                        self.settings_menu()

                    if buttons['quit_button'].check_for_input(menu_mouse_pos):
                        quit_game()

            pygame.display.update()

    def create_main_menu_texts(self) -> None:
        self.create_text(TITLE_FONT_SIZE, 'MAIN MENU', '#b68f40', (400, 200))

    def run_game(self) -> None:
        self.play_game = True
        self.display_main_menu = False
        check_if_random_position()
        game = Game(self.game_window, settings)
        game.run()
        self.back_to_main_menu()

    def settings_menu(self) -> None:
        self.set_options = True
        self.display_main_menu = False

        while self.set_options:
            self.game_window.fill('black')
            menu_mouse_pos = pygame.mouse.get_pos()
            # print(menu_mouse_pos)

            self.create_settings_texts()

            buttons = create_settings_buttons()

            for button in buttons.values():
                button.change_color(menu_mouse_pos)
                button.update(self.game_window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

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
                    if buttons['select_car_previous_button'].check_for_input(menu_mouse_pos):
                        index_of_current_car = CARS.index(settings.selected_car)

                        if index_of_current_car > 0:
                            settings.selected_car = CARS[index_of_current_car - 1]
                            settings.selected_car_name = CAR_NAMES[index_of_current_car - 1]

                    if buttons['select_car_next_button'].check_for_input(menu_mouse_pos):
                        index_of_current_car = CARS.index(settings.selected_car)

                        if index_of_current_car < len(CARS) - 1:
                            settings.selected_car = CARS[index_of_current_car + 1]
                            settings.selected_car_name = CAR_NAMES[index_of_current_car + 1]

                    if buttons['select_track_previous_button'].check_for_input(menu_mouse_pos):
                        index_of_current_track = TRACKS.index(settings.selected_track)

                        if index_of_current_track > 0:
                            settings.selected_track = TRACKS[index_of_current_track - 1]
                            settings.selected_track_name = TRACK_NAMES[index_of_current_track - 1]

                    if buttons['select_track_next_button'].check_for_input(menu_mouse_pos):
                        index_of_current_track = TRACKS.index(settings.selected_track)

                        if index_of_current_track < len(TRACKS) - 1:
                            settings.selected_track = TRACKS[index_of_current_track + 1]
                            settings.selected_track_name = TRACK_NAMES[index_of_current_track + 1]

                    if buttons['select_laps_previous_button'].check_for_input(menu_mouse_pos):
                        index_of_current_lap = LAPS.index(settings.selected_laps)

                        if index_of_current_lap > 0:
                            settings.selected_laps = LAPS[index_of_current_lap - 1]

                    if buttons['select_laps_next_button'].check_for_input(menu_mouse_pos):
                        index_of_current_lap = LAPS.index(settings.selected_laps)

                        if index_of_current_lap < len(LAPS) - 1:
                            settings.selected_laps = LAPS[index_of_current_lap + 1]

                    if buttons['select_opponents_previous_button'].check_for_input(menu_mouse_pos):
                        index_of_current_opponents = OPPONENTS.index(settings.opponents)

                        if index_of_current_opponents > 0:
                            settings.opponents = OPPONENTS[index_of_current_opponents - 1]

                    if buttons['select_opponents_next_button'].check_for_input(menu_mouse_pos):
                        index_of_current_opponents = OPPONENTS.index(settings.opponents)

                        if index_of_current_opponents < len(OPPONENTS) - 1:
                            settings.opponents = OPPONENTS[index_of_current_opponents + 1]

                    if buttons['select_opponents_level_previous_button'].check_for_input(menu_mouse_pos):
                        index_of_current_opponents_level = OPPONENTS_LEVEL.index(settings.opponents_level)

                        if index_of_current_opponents_level > 0:
                            settings.opponents_level = OPPONENTS_LEVEL[index_of_current_opponents_level - 1]

                    if buttons['select_opponents_level_next_button'].check_for_input(menu_mouse_pos):
                        index_of_current_opponents_level = OPPONENTS_LEVEL.index(settings.opponents_level)

                        if index_of_current_opponents_level < len(OPPONENTS_LEVEL) - 1:
                            settings.opponents_level = OPPONENTS_LEVEL[index_of_current_opponents_level + 1]

                    if buttons['select_starting_position_previous_button'].check_for_input(menu_mouse_pos):
                        index_of_current_starting_position = STARTING_POSITIONS.index(settings.starting_position)

                        if index_of_current_starting_position > 0:
                            settings.starting_position = STARTING_POSITIONS[index_of_current_starting_position - 1]

                    if buttons['select_starting_position_next_button'].check_for_input(menu_mouse_pos):
                        index_of_current_starting_position = STARTING_POSITIONS.index(settings.starting_position)

                        if index_of_current_starting_position < len(STARTING_POSITIONS) - 1:
                            settings.starting_position = STARTING_POSITIONS[index_of_current_starting_position + 1]

                    if buttons['back_button'].check_for_input(menu_mouse_pos):
                        self.back_to_main_menu()

            pygame.display.update()

    def back_to_main_menu(self) -> None:
        self.play_game = False
        self.set_options = False
        self.display_main_menu = True
        self.main_menu()

    def create_settings_texts(self) -> None:
        self.create_text(TITLE_FONT_SIZE, 'SETTINGS', '#b68f40', (400, 100))
        self.create_text(SELECTION_FONT_SIZE, 'NAME', position=(450, 250), positioning='midright')
        self.create_text(SELECTION_FONT_SIZE, settings.player_nickname, position=(600, 250))
        self.create_text(SELECTION_FONT_SIZE, 'CAR', position=(450, 300), positioning='midright')
        self.create_text(SELECTION_FONT_SIZE, settings.selected_car_name, position=(600, 300))
        self.create_text(SELECTION_FONT_SIZE, 'TRACK', position=(450, 350), positioning='midright')
        self.create_text(SELECTION_FONT_SIZE, settings.selected_track_name, position=(600, 350))
        self.create_text(SELECTION_FONT_SIZE, 'LAPS', position=(450, 400), positioning='midright')
        self.create_text(SELECTION_FONT_SIZE, str(settings.selected_laps), position=(600, 400))
        self.create_text(SELECTION_FONT_SIZE, 'OPPONENTS', position=(450, 450), positioning='midright')
        self.create_text(SELECTION_FONT_SIZE, str(settings.opponents), position=(600, 450))
        self.create_text(SELECTION_FONT_SIZE, 'OPPONENTS LEVEL', position=(450, 500), positioning='midright')
        self.create_text(SELECTION_FONT_SIZE, str(settings.opponents_level), position=(600, 500))
        self.create_text(SELECTION_FONT_SIZE, 'STARTING POSITION', position=(450, 550), positioning='midright')
        self.create_text(SELECTION_FONT_SIZE, str(settings.starting_position), position=(600, 550))

    # create text positioned by its center
    def create_text(
            self,
            font_size: int = MAIN_FONT_SIZE,
            text: str = 'SAMPLE TEXT',
            color: str = '#d7fcd4',
            position: tuple[int, int] = (400, 400),
            positioning: str = 'center'
    ) -> None:
        text = get_font(font_size).render(text, True, color)

        if positioning == 'midleft':
            text_rect = text.get_rect(midleft=position)
        elif positioning == 'midright':
            text_rect = text.get_rect(midright=position)
        else:
            text_rect = text.get_rect(center=position)

        self.game_window.blit(text, text_rect)