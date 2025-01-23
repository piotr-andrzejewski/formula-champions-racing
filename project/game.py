# main game

import sys
import time

import pygame.time
from pygame.display import get_surface

from cars import *
from images import FINISH_LINE, TRACK_1_LIMITS, LIGHTS
from settings import *
from utils import blit_screen

mili = 1000

# constants for the game
TRACK_1_POSITION = (10, 10)
TRACK_1_LIMITS_POSITION = (10, 10)
TRACK_1_FINISH_LINE_POSITION = (535, 762)

# create font for on screen messages
pygame.font.init()
GAME_FONT = pygame.font.Font('./assets/Space_Bd_BT_Bold.ttf', 36)
GAME_FONT.render('START', True, (255, 255, 255), (0, 0, 0))

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

    def reset(self) -> None:
        self.started = False
        self.game_start_time = 0.0
        self.game_total_time = 0.0
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
        for i in range(len(lights)):
            self.game_window.blit(lights[i],(400, 400))
            pygame.display.update()
            time.sleep(1)

        self.game_window.blit(lights[0], (400, 400))
        pygame.display.update()
        blit_screen(self.game_window)

    def start_game(self) -> None:
        self.game_window.fill((0, 70, 0))
        self.draw()
        self.count_to_start_race(LIGHTS)
        self.game_window.fill((0, 70, 0))
        self.started = True
        self.game_start_time = time.time_ns() / mili

    def end_game(self) -> None:
        self.get_best_lap()
        self.get_game_total_time()
        print('Laps completed:')
        print('Player: ', self.player.completed_laps)

        for i in range(len(self.opponents)):
            print(f'Opponent {i + 1}: ', self.opponents[i].completed_laps)

            # # code to display computer car's path in console to be able to copy it for PATH variable
            # print(opponents[i].path)

        self.reset()

    def get_game_total_time(self) -> None:
        self.game_total_time = round(time.time_ns() / mili - self.game_start_time)
        print(f'Total time: {self.game_total_time}')

    def run(self) -> None:
        self.start_game()

        # main loop for the game
        while self.started:

            # set max fps for the game
            CLOCK.tick(FPS)
            # mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():

                # check the event of user clicking 'X' button to close the game window
                if event.type == pygame.QUIT:
                    self.end_game()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.end_game()

                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     print(mouse_pos)

            self.draw()
            self.move_player()
            # generate_path_for_computer_car()

            self.handle_collisions()
            self.handle_finish_line_crossing()

            if self.player.completed_laps == self.settings.selected_laps:
                self.end_game()

            pygame.display.update()

    def draw(self, track_name: str = "TRACK 1") -> None:
        if self.player.crossed_line:
            self.game_window.fill((0, 70, 0))

        if track_name == "TRACK 1":
            for img, pos in TRACK_1_IMAGES:
                self.game_window.blit(img, pos)
        # elif track_name == "TRACK 2":
        #     for img, pos in TRACK_2_IMAGES:
        #         self.game_window.blit(img, pos)
        # elif track_name == "TRACK 3":
        #     for img, pos in TRACK_3_IMAGES:
        #         self.game_window.blit(img, pos)

        self.player.draw(self.game_window)

        for opponent in self.opponents:
            opponent.draw(self.game_window)

        pygame.display.update()

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

    def handle_collisions(self) -> None:

        # TODO: handle track limits for potential penalties when player turns on such option
        if self.player.collide(TRACK_1_LIMITS_MASK, *TRACK_1_LIMITS_POSITION) is None:
            print('Get back to track')

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
                print('Wrong way')
                self.player.reset_position()

        if player_finish_line_poi is None:
            if self.player.crossed_line:
                current_time = time.time_ns() / mili
                self.player.completed_laps += 1
                self.player.lap_times.append(round(current_time - self.player.lap_start_time))
                self.player.lap_start_time = current_time
                self.player.crossed_line = False
                print('Lap completed')

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
            print(mouse_pos)

            # select index of computer car for which you want to create path
            i = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.opponents[i].path.append(mouse_pos)

            # code to delete last path point
            if event.type == pygame.KEYDOWN:
                if pressed_keys[pygame.K_c]:
                    self.opponents[i].path.pop()

            # code to add many points from player's position
            if pressed_keys[pygame.K_SPACE]:
                self.opponents[i].path.append((self.player.x_pos, self.player.y_pos))

    def get_best_lap(self) -> None:
        self.player.find_best_lap()

        if self.player.best_lap is not None:
            print(f'Best lap: {self.player.best_lap}')