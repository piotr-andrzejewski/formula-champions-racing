# main game

import sys
import time

import pygame.time
from pygame import KEYDOWN
from pygame.display import get_surface

from cars import *
from images import FINISH_LINE, TRACK_1_LIMITS, LIGHTS, FLAG_FINISH
from settings import *
from utils import *

# constants for the game
TRACK_1_POSITION = (10, 10)
TRACK_1_LIMITS_POSITION = (10, 10)
TRACK_1_FINISH_LINE_POSITION = (535, 762)

# set frames per second parameter
FPS = 60
CLOCK = pygame.time.Clock()

TRACK_1_IMAGES = [
    (TRACK_1_LIMITS, TRACK_1_LIMITS_POSITION),
    (TRACK_1, TRACK_1_POSITION),
    (FINISH_LINE, TRACK_1_FINISH_LINE_POSITION)
]

TRACK_1_LIMITS_MASK = pygame.mask.from_surface(TRACK_1_LIMITS)
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE)


class Game:
    def __init__(self, game_window: Surface, settings: Settings) -> None:
        self.game_window = game_window
        self.settings = settings
        self.player = self.generate_player()
        self.opponents = self.generate_opponents()
        self.started = False
        self.game_start_time = 0.0
        self.game_total_time = 0.0
        self.start_time_out_of_track = 0.0
        self.time_out_of_track = 0.0
        self.penalty = False

    def reset(self) -> None:
        self.started = False
        self.game_start_time = 0.0
        self.game_total_time = 0.0
        self.start_time_out_of_track = 0.0
        self.time_out_of_track = 0.0
        self.penalty = False
        self.player.reset()
        self.settings.occupied_starting_positions = []

        for opponent in self.opponents:
            opponent.reset()

    def generate_player(self) -> PlayerCar:
        return PlayerCar(img=self.settings.selected_car, start_pos=self.settings.get_player_starting_track_position())

    def generate_opponents(self) -> list[ComputerCar]:
        occupied_cars = [self.settings.selected_car]
        opponents = []

        for i in range(self.settings.opponents):
            computer_car = get_opponent_car(occupied_cars)
            opponents.append(
                ComputerCar(
                    img=computer_car,
                    level=self.settings.opponents_level,
                    start_pos=self.settings.get_opponent_starting_track_position()
                )
            )
            occupied_cars.append(computer_car)

        return opponents

    def count_to_start_race(self, lights: dict[int, Surface] = LIGHTS) -> None:
        x_pos = 350
        y_pos = 350
        self.game_window.fill((0, 70, 0))
        self.draw()

        # for i in range(len(lights)):
        #     self.check_events()
        #     self.game_window.blit(lights[i],(x_pos, y_pos))
        #     pygame.display.update()
        #     time.sleep(1)
        #
        # self.game_window.blit(lights[0], (x_pos, y_pos))
        # pygame.display.update()
        # blit_screen(self.game_window)
        # self.game_window.fill((0, 70, 0))

        self.started = True

    def start_game(self) -> None:
        self.game_window.fill((0, 70, 0))
        self.draw()
        create_text(
            self.game_window,
            SECONDARY_FONT_SIZE,
            "PRESS SPACE KEY TO START",
            color='#b68f40',
            position=(400, 400)
        )
        pygame.display.update()
        started = False

        while not started:
            self.check_events()

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

                if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                    started = True

        self.count_to_start_race()
        current_time = round(time.time(), 3)
        self.game_start_time = current_time
        self.player.lap_start_time = current_time

    def end_game(self) -> None:
        # print('Laps completed:')
        # print('Player: ', self.player.completed_laps)
        #
        # for i in range(len(self.opponents)):
        #     print(f'Opponent {i + 1}: ', self.opponents[i].completed_laps)
        #
        #     # # code to display computer car's path in console to be able to copy it for PATH variable
        #     # print(opponents[i].path)

        self.reset()

    def get_lap_time(self) -> int:
        return round(time.time() - self.player.lap_start_time, 3)

    def get_game_total_time(self) -> float:
        current_time = round(time.time() - self.game_start_time, 3)
        self.game_total_time = current_time

        return current_time

    def run(self) -> None:
        self.start_game()

        # main loop for the game
        while self.started:
            # mouse_pos = pygame.mouse.get_pos()

            # set max fps for the game
            CLOCK.tick(FPS)

            self.check_events()
            self.draw()
            self.move_player()

            self.generate_path_for_computer_car()

            self.handle_out_of_track()
            self.handle_finish_line_crossing()

            if self.player.completed_laps == self.settings.selected_laps:
                self.show_results()

            if self.player.out_of_track:
                self.determine_penalty(self.time_out_of_track)
                if self.penalty:
                    self.display_penalty_text(self.penalty)
                    self.player.score -= 1

            pygame.display.update()

    def check_events(self, buttons: dict[str, Button] = None, mouse_pos: tuple[int, int] = (0, 0)) -> None:
        for event in pygame.event.get():

            # check the event of user clicking 'X' button to close the game window
            if event.type == pygame.QUIT:
                self.end_game()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.end_game()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.started = True

            if event.type == pygame.MOUSEBUTTONDOWN:
            #     print(mouse_pos)

                if buttons:
                    if buttons['back'].check_for_input(mouse_pos):
                        self.end_game()

    def draw(self) -> None:
        self.game_window.fill((0, 70, 0))
        self.draw_track(self.settings.selected_track_name)
        self.display_info()

        if self.player.out_of_track:
            self.display_back_to_track_text()

        self.player.draw(self.game_window)

        for opponent in self.opponents:
            opponent.draw(self.game_window)

        pygame.display.update()

    def draw_track(self, track_name: str = 'TRACK 1') -> None:
        if track_name == 'TRACK 1':
            for img, pos in TRACK_1_IMAGES:
                self.game_window.blit(img, pos)
        # elif track_name == "TRACK 2":
        #     for img, pos in TRACK_2_IMAGES:
        #         self.game_window.blit(img, pos)
        # elif track_name == "TRACK 3":
        #     for img, pos in TRACK_3_IMAGES:
        #         self.game_window.blit(img, pos)

    def move_player(self) -> None:
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_w]:
            moved = True
            self.player.move_forward()
            if keys[pygame.K_a]:
                self.player.rotate(left=True)
            elif keys[pygame.K_d]:
                self.player.rotate(right=True)
        elif keys[pygame.K_s]:
            moved = True
            if self.player.vel <= 0:
                self.player.reverse()
                if keys[pygame.K_a]:
                    self.player.rotate(right=True)
                elif keys[pygame.K_d]:
                    self.player.rotate(left=True)
            else:
                self.player.brake()
                if keys[pygame.K_a]:
                    self.player.rotate(left=True)
                elif keys[pygame.K_d]:
                    self.player.rotate(right=True)

        if not moved:
            self.player.reduce_speed()
            if self.player.vel != 0:
                if keys[pygame.K_a]:
                    self.player.rotate(left=True)
                elif keys[pygame.K_d]:
                    self.player.rotate(right=True)

    def handle_out_of_track(self) -> None:
        if self.player.collide(TRACK_1_LIMITS_MASK, *TRACK_1_LIMITS_POSITION) is None:
            self.player.out_of_track = True

            if self.start_time_out_of_track == 0.0:
                self.start_time_out_of_track = round(time.time(), 3)
            else:
                self.time_out_of_track = round(time.time() - self.start_time_out_of_track, 3)
        else:
            self.player.out_of_track = False
            self.start_time_out_of_track = 0.0
            self.time_out_of_track = 0.0

    def handle_finish_line_crossing(self) -> None:
        for opponent in self.opponents:
            opponent_finish_line_poi = opponent.collide(FINISH_LINE_MASK, *TRACK_1_FINISH_LINE_POSITION)

            if opponent_finish_line_poi is not None:
                opponent.crossed_line = True
                opponent.current_point = 0

            if opponent_finish_line_poi is None:
                if opponent.crossed_line:
                    opponent.completed_laps += 1
                    opponent.crossed_line = False

        player_finish_line_poi = self.player.collide(FINISH_LINE_MASK, *TRACK_1_FINISH_LINE_POSITION)

        if player_finish_line_poi is not None:
            if player_finish_line_poi[0] > 0:
                self.player.crossed_line = True

            if not self.player.crossed_line:
                self.display_wrong_way_text()
                self.player.reset_position()

        if player_finish_line_poi is None:
            if self.player.crossed_line:
                current_time = round(time.time(), 3)
                self.player.completed_laps += 1
                self.player.lap_times.append(round(current_time - self.player.lap_start_time, 3))
                self.player.lap_start_time = current_time
                self.player.crossed_line = False

    def generate_path_for_computer_car(self) -> None:
        pressed_keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            # code to generate points for computer car path
            if event.type == pygame.KEYDOWN:
                if pressed_keys[pygame.K_x]:

                    # display player position to better tune computer car's path
                    print((self.player.x_pos, self.player.y_pos))

            # code to get coordinates of mouse position
            mouse_pos = pygame.mouse.get_pos()

            # select index of computer car for which you want to create path
            i = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(mouse_pos)

            #     self.opponents[i].path.append(mouse_pos)
            #
            # # code to delete last path point
            # if event.type == pygame.KEYDOWN:
            #     if pressed_keys[pygame.K_c]:
            #         self.opponents[i].path.pop()
            #
            # # code to add many points from player's position
            # if pressed_keys[pygame.K_SPACE]:
            #     self.opponents[i].path.append((self.player.x_pos, self.player.y_pos))

    def get_best_lap(self) -> float | None:
        self.player.find_best_lap()

        if self.player.best_lap is not None:
            return self.player.best_lap

    def show_results(self) -> None:
        box = pygame.Surface((400, 450), masks=(0, 0, 0))
        self.game_window.blit(box, (200, 200))
        pygame.display.update()

        self.get_best_lap()
        self.get_game_total_time()

        while self.started:
            mouse_pos = pygame.mouse.get_pos()
            self.create_results_texts()
            self.game_window.blit(FLAG_FINISH, (470, 225))

            back_button = self.create_back_button()
            back_button.change_color(mouse_pos)
            back_button.update(self.game_window)

            self.check_events(buttons={'back': back_button}, mouse_pos=mouse_pos)

            pygame.display.update()

    def display_info(self) -> None:
        left_pos = 720
        right_pos = 785
        top_pos = 100
        interval = 30
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'LAP:',
            position=(left_pos, top_pos),
            positioning='midright'
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'LAP TIME:',
            position=(left_pos, top_pos + interval),
            positioning='midright'
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'TOTAL TIME:',
            position=(left_pos, top_pos + interval * 2),
            positioning='midright'
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            'VELOCITY:',
            position=(left_pos, top_pos + interval * 3),
            positioning='midright'
        )
        create_text(
            self.game_window,
            GAME_INFO_FONT_SIZE,
            str(round(self.player.vel, 2)),
            position=(right_pos, top_pos + interval * 3),
            positioning='midright'
        )

        if self.started:
            create_text(
                self.game_window,
                GAME_INFO_FONT_SIZE,
                str(self.player.completed_laps + 1) + ' / ' + str(self.settings.selected_laps),
                position=(right_pos, top_pos),
                positioning='midright'
            )
            create_text(
                self.game_window,
                GAME_INFO_FONT_SIZE,
                str(self.get_lap_time()),
                position=(right_pos, top_pos + interval),
                positioning='midright'
            )
            create_text(
                self.game_window,
                GAME_INFO_FONT_SIZE,
                str(self.get_game_total_time()),
                position=(right_pos, top_pos + interval * 2),
                positioning='midright'
            )
        else:
            create_text(
                self.game_window,
                GAME_INFO_FONT_SIZE,
                str(self.player.completed_laps) + ' / ' + str(self.settings.selected_laps),
                position=(right_pos, top_pos),
                positioning='midright'
            )
            create_text(
                self.game_window,
                GAME_INFO_FONT_SIZE,
                str(self.player.lap_start_time),
                position=(right_pos, top_pos + interval),
                positioning='midright'
            )
            create_text(
                self.game_window,
                GAME_INFO_FONT_SIZE,
                str(self.game_total_time),
                position=(right_pos, top_pos + interval * 2),
                positioning='midright'
            )

    def display_back_to_track_text(self) -> None:
        create_text(
            self.game_window,
            SECONDARY_FONT_SIZE,
            'GET BACK TO TRACK',
            color='#b68f40',
            position=(400, 400)
        )

    def display_wrong_way_text(self) -> None:
        create_text(
            self.game_window,
            SECONDARY_FONT_SIZE,
            'WRONG WAY',
            color='#b68f40',
            position=(400, 400)
        )

    def determine_penalty(self, time_out_of_track: float = 0.0) -> None:
        if self.settings.penalties == 'ON':
            if self.player.corner_cut(COLLISION_POINTS['TRACK 1']):
                self.penalty = True

                return

            if time_out_of_track == 0.0:
                return

            penalty_threshold = 5.0

            if time_out_of_track > penalty_threshold:
                self.penalty = True
            else:
                self.penalty = False

        return

    def display_penalty_text(self, penalty: bool = False) -> None:
        if not penalty:
            return

        create_text(
            self.game_window,
            SECONDARY_FONT_SIZE,
            'PENALTY',
            color='#b68f40',
            position=(400, 300)
        )

    def create_results_texts(self) -> None:
        left_pos, right_pos = 225, 575
        top_pos = 335
        interval = 50
        create_text(
            self.game_window,
            SECONDARY_FONT_SIZE,
            'RESULTS',
            color='#b68f40',
            position=(left_pos, 260),
            positioning='midleft'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'POSITION',
            position=(left_pos, top_pos),
            positioning='midleft'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(self.player.final_position) + ' / ' + str(self.settings.opponents + 1),
            position=(right_pos, top_pos),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'COMPLETED LAPS',
            position=(left_pos, top_pos + interval),
            positioning='midleft'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(self.player.completed_laps) + ' / ' + str(self.settings.selected_laps),
            position=(right_pos, top_pos + interval),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            'BEST LAP',
            position=(left_pos, top_pos + 2 * interval),
            positioning='midleft'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(self.player.best_lap),
            position=(right_pos, top_pos + 2 * interval),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            "TOTAL TIME",
            position=(left_pos, top_pos + 3 * interval),
            positioning='midleft'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(self.game_total_time),
            position=(right_pos, top_pos + 3 * interval),
            positioning='midright'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            "SCORE",
            position=(left_pos, top_pos + 4 * interval),
            positioning='midleft'
        )
        create_text(
            self.game_window,
            SELECTION_FONT_SIZE,
            str(self.player.score),
            position=(right_pos, top_pos + 4 * interval),
            positioning='midright'
        )

    @staticmethod
    def create_back_button() -> Button:
        return Button(
            position=(400, 600),
            text_input='BACK',
            font=get_font(SELECTION_FONT_SIZE),
            base_color='#d7fcd4',
            hover_color='white'
        )
