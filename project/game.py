# main game

import sys
import time

import pygame.constants
import pygame.display
import pygame.event
import pygame.key
import pygame.mouse
import pygame.time
from pygame.surface import Surface
from pygame.mask import MaskType

from cars import COLLISION_POINTS, calculate_vel_factor, PlayerCar, ComputerCar
from images import FINISH_LINE, FLAG_FINISH, FLAG_PENALTY, LIGHTS, TRACK_1, TRACK_2, TRACK_3, TRACK_1_LIMITS, \
    TRACK_2_LIMITS, TRACK_3_LIMITS
from settings import LAPS, Settings
from utils import GAME_INFO_FONT_SIZE, SECONDARY_FONT_SIZE, SELECTION_FONT_SIZE, \
    blit_screen, create_button, create_text, read_highscores_file, update_highscores_file

# constants for the game
TRACK_1_POSITION = (-40, -20)
TRACK_1_FINISH_LINE_POSITION = (635, 733)
TRACK_2_POSITION = (-45, -50)
TRACK_2_FINISH_LINE_POSITION = (755, 583)
TRACK_3_POSITION = (-140, -80)
TRACK_3_FINISH_LINE_POSITION = (400, 233)

# set frames per second parameter
FPS = 60
CLOCK = pygame.time.Clock()

TRACK_1_IMAGES = [
    (TRACK_1_LIMITS, TRACK_1_POSITION),
    (TRACK_1, TRACK_1_POSITION),
    (FINISH_LINE, TRACK_1_FINISH_LINE_POSITION)
]
TRACK_2_IMAGES = [
    (TRACK_2_LIMITS, TRACK_2_POSITION),
    (TRACK_2, TRACK_2_POSITION),
    (FINISH_LINE, TRACK_2_FINISH_LINE_POSITION)
]
TRACK_3_IMAGES = [
    (TRACK_3_LIMITS, TRACK_3_POSITION),
    (TRACK_3, TRACK_3_POSITION),
    (FINISH_LINE, TRACK_3_FINISH_LINE_POSITION)
]

TRACK_1_LIMITS_MASK = pygame.mask.from_surface(TRACK_1_LIMITS)
TRACK_2_LIMITS_MASK = pygame.mask.from_surface(TRACK_2_LIMITS)
TRACK_3_LIMITS_MASK = pygame.mask.from_surface(TRACK_3_LIMITS)
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

        for key, opponent in self.opponents.items():
            opponent.reset()

    def generate_player(self) -> PlayerCar:
        return PlayerCar(img=self.settings.selected_car, start_pos=self.settings.get_player_starting_track_position())

    def generate_opponents(self) -> dict[int, ComputerCar]:
        occupied_cars = [self.settings.selected_car]
        opponents = {}

        for i in range(self.settings.opponents):
            computer_car = self.settings.get_opponent_car(occupied_cars)
            opponents[i] = ComputerCar(
                img=computer_car,
                level=self.settings.opponents_level,
                start_pos=self.settings.get_opponent_starting_track_position(),
                track_name=self.settings.selected_track_name
            )
            occupied_cars.append(computer_car)

        return opponents

    def count_to_start_race(self, lights: dict[int, Surface] = LIGHTS) -> None:
        x_pos = self.game_window.get_width() / 2 - 50
        y_pos = 350
        self.game_window.fill((0, 70, 0))
        self.draw()

        for i in range(len(lights)):
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    self.end_game()
                    sys.exit()

                if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_ESCAPE:
                    return

            self.game_window.blit(lights[i],(x_pos, y_pos))
            pygame.display.update()
            time.sleep(1)

        self.game_window.blit(lights[0], (x_pos, y_pos))
        pygame.display.update()
        blit_screen(self.game_window)
        self.game_window.fill((0, 70, 0))

        self.started = True

    def start_game(self) -> None:
        self.game_window.fill((0, 70, 0))
        self.draw()
        create_text(
            self.game_window,
            SECONDARY_FONT_SIZE,
            "PRESS SPACE KEY TO START",
            color='#b68f40',
            position=(self.game_window.get_width() / 2, self.game_window.get_height() / 2)
        )
        pygame.display.update()
        started = False

        while not started:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    self.end_game()
                    sys.exit()

                if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_ESCAPE:
                    return

                if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_SPACE:
                    started = True

        self.count_to_start_race()
        current_time = round(time.time(), 3)
        self.game_start_time = current_time
        self.player.lap_start_time = current_time

    def end_game(self) -> None:
        self.reset()

    def get_lap_time(self) -> int:
        return round(time.time() - self.player.lap_start_time, 3)

    def get_game_total_time(self) -> float:
        current_time = round(time.time() - self.game_start_time, 3)
        self.game_total_time = current_time

        return current_time

    def generate_path_for_computer_car(self) -> None:
        pressed_keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.constants.MOUSEBUTTONDOWN:
                print(mouse_pos)

            # code to generate points for computer car path
            if event.type == pygame.constants.KEYDOWN:
                if pressed_keys[pygame.constants.K_x]:

                    # display player position to better tune computer car's path
                    print((self.player.x_pos, self.player.y_pos))

    def run(self) -> None:
        self.start_game()

        # main loop for the game
        while self.started:

            # set max fps for the game
            CLOCK.tick(FPS)

            self.draw()
            self.move_player()
            self.determine_track_specific_conditions()

            if self.player.out_of_track:
                self.determine_penalty(self.settings.selected_track_name, self.time_out_of_track)
                if self.penalty:
                    self.display_penalty_text(self.penalty)
                    self.player.score -= 50

            if self.player.score < 0:
                self.player.score = 0

            if self.player.completed_laps == self.settings.selected_laps:
                for key, opponent in self.opponents.items():
                    if opponent.completed_laps == self.settings.selected_laps:
                        self.player.final_position += 1

                self.show_results()

            pygame.display.update()

    def draw(self) -> None:
        self.game_window.fill((0, 70, 0))
        self.draw_track(self.settings.selected_track_name)
        self.display_info()

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                self.end_game()
                sys.exit()

            if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_ESCAPE:
                self.end_game()

            # next three if statements are dedicated to generating path for computer car to follow
            if event.type == pygame.constants.MOUSEBUTTONDOWN:
                print(mouse_pos)

            # code to generate points for computer car path
            if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_x:

                # display player position to better tune computer car's path
                print((self.player.x_pos, self.player.y_pos))

            # manipulating path when there is at least one opponent active
            if self.opponents:

                # select index of computer car for which you want to create path
                i = 0

                if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_z:
                    self.opponents[i].path.append((self.player.x_pos, self.player.y_pos))

                # code to delete last path point
                if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_c:
                    self.opponents[i].path.pop()

        if self.player.out_of_track:
            self.display_back_to_track_text()

        self.player.draw(self.game_window)

        for key, opponent in self.opponents.items():
            opponent.draw(self.game_window)

        pygame.display.update()

    def draw_track(self, track_name: str) -> None:
        if track_name == 'TRACK 1':
            for img, pos in TRACK_1_IMAGES:
                self.game_window.blit(img, pos)
        elif track_name == "TRACK 2":
            for img, pos in TRACK_2_IMAGES:
                self.game_window.blit(img, pos)
        elif track_name == "TRACK 3":
            for img, pos in TRACK_3_IMAGES:
                self.game_window.blit(img, pos)

    def move_player(self) -> None:
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.constants.K_w]:
            moved = True
            self.player.move_forward()
            if keys[pygame.constants.K_a]:
                self.player.rotate(left=True)
            elif keys[pygame.constants.K_d]:
                self.player.rotate(right=True)
        elif keys[pygame.constants.K_s]:
            moved = True
            if self.player.vel <= 0:
                self.player.reverse()
                if keys[pygame.constants.K_a]:
                    self.player.rotate(right=True)
                elif keys[pygame.constants.K_d]:
                    self.player.rotate(left=True)
            else:
                self.player.brake()
                if keys[pygame.constants.K_a]:
                    self.player.rotate(left=True)
                elif keys[pygame.constants.K_d]:
                    self.player.rotate(right=True)

        if not moved:
            self.player.reduce_speed()
            if self.player.vel != 0:
                if keys[pygame.constants.K_a]:
                    self.player.rotate(left=True)
                elif keys[pygame.constants.K_d]:
                    self.player.rotate(right=True)

    def determine_track_specific_conditions(self) -> None:
        if self.settings.selected_track_name == 'TRACK 1':
            self.handle_out_of_track(TRACK_1_LIMITS_MASK, TRACK_1_POSITION)
            self.handle_finish_line_crossing(TRACK_1_FINISH_LINE_POSITION)
        elif self.settings.selected_track_name == 'TRACK 2':
            self.handle_out_of_track(TRACK_2_LIMITS_MASK, TRACK_2_POSITION)
            self.handle_finish_line_crossing(TRACK_2_FINISH_LINE_POSITION)
        elif self.settings.selected_track_name == 'TRACK 3':
            self.handle_out_of_track(TRACK_3_LIMITS_MASK, TRACK_3_POSITION)
            self.handle_finish_line_crossing(TRACK_3_FINISH_LINE_POSITION, inverse=True)

    def handle_out_of_track(self, track_limits_mask: MaskType, track_limits_pos: tuple[int, int]) -> None:
        if self.player.collide(track_limits_mask, *track_limits_pos) is None:
            self.player.out_of_track = True

            if self.start_time_out_of_track == 0.0:
                self.start_time_out_of_track = round(time.time(), 3)
            else:
                self.time_out_of_track = round(time.time() - self.start_time_out_of_track, 3)
        else:
            self.player.out_of_track = False
            self.start_time_out_of_track = 0.0
            self.time_out_of_track = 0.0

    def handle_finish_line_crossing(self, track_finish_line_pos: tuple[int, int], inverse: bool = False) -> None:
        time_interval = 10

        for key, opponent in self.opponents.items():
            opponent_finish_line_poi = opponent.collide(FINISH_LINE_MASK, *track_finish_line_pos)

            if inverse:
                if opponent_finish_line_poi is not None:
                    opponent.crossed_start_line = True
            else:
                opponent.crossed_start_line = True

            if opponent.crossed_start_line and self.get_game_total_time() > time_interval:
                if opponent_finish_line_poi is not None:
                    opponent.crossed_finish_line = True
                    opponent.current_point = 0

                if opponent_finish_line_poi is None:
                    if opponent.crossed_finish_line:
                        opponent.completed_laps += 1
                        opponent.crossed_finish_line = False

        player_finish_line_poi = self.player.collide(FINISH_LINE_MASK, *track_finish_line_pos)

        if inverse:
            if player_finish_line_poi is not None:
                self.player.crossed_start_line = True
        else:
            self.player.crossed_start_line = True

        if self.player.crossed_start_line:
            if player_finish_line_poi is not None:
                if player_finish_line_poi[0] > 0 and self.get_game_total_time() > time_interval:
                    self.player.crossed_finish_line = True

                if not self.player.crossed_finish_line and self.get_game_total_time() > time_interval / 2:
                    self.display_wrong_way_text()
                    self.player.reset_position(self.settings.selected_track_name)

            if player_finish_line_poi is None:
                if self.player.crossed_finish_line:
                    current_time = round(time.time(), 3)
                    self.player.completed_laps += 1
                    self.player.lap_times.append(round(current_time - self.player.lap_start_time, 3))
                    self.player.lap_start_time = current_time
                    self.player.crossed_finish_line = False

    def get_best_lap(self) -> float | None:
        self.player.find_best_lap()

        if self.player.best_lap is not None:
            return self.player.best_lap

    def calculate_score(self) -> None:
        if self.settings.selected_track_name == 'TRACK 3':
            track_factor = 1.0
        elif self.settings.selected_track_name == 'TRACK 2':
            track_factor = 0.96
        else:
            track_factor = 0.98

        if self.settings.opponents_level == 1:
            opponents_level_factor = 0.6
        elif self.settings.opponents_level == 2:
            opponents_level_factor = 0.8
        else:
            opponents_level_factor = 1

        if self.settings.starting_position < 5:
            starting_position_factor = 0.8
        else:
            starting_position_factor = 1

        if self.player.final_position == 1:
            final_position_factor = 1
        elif self.player.final_position == 2:
            final_position_factor = 0.9
        elif self.player.final_position == 3:
            final_position_factor = 0.8
        elif self.player.final_position == 4:
            final_position_factor = 0.7
        elif self.player.final_position == 5:
            final_position_factor = 0.6
        elif self.player.final_position == 6:
            final_position_factor = 0.5
        elif self.player.final_position == 7:
            final_position_factor = 0.4
        else:
            final_position_factor = 0.3

        total_time_factor = 0.5

        for i in range(1, len(LAPS)):
            if self.settings.selected_laps == i:
                if self.game_total_time <= 45.0 * i:
                    total_time_factor = 1
                elif self.game_total_time <= 60.0 * i:
                    total_time_factor = 0.75
                else:
                    total_time_factor = 0.5
                break

        if self.settings.penalties == 'ON':
            penalties_factor = 1
        else:
            penalties_factor = 0.5

        car_factor = calculate_vel_factor(self.player.img)

        self.player.score = round(
                1000
                * 60
                * track_factor
                * opponents_level_factor
                * starting_position_factor
                * final_position_factor
                * total_time_factor
                * penalties_factor
                * self.settings.selected_laps
                / car_factor
                / self.game_total_time
        )

    def show_results(self) -> None:
        box = Surface((self.game_window.get_width() / 2 - 100, 450), masks=(0, 0, 0))
        self.game_window.blit(box, (self.game_window.get_width() / 2 - 200, 200))
        pygame.display.update()

        self.get_best_lap()
        self.get_game_total_time()
        self.calculate_score()
        self.save_score()

        while self.started:
            self.create_results_texts()
            self.game_window.blit(FLAG_FINISH, (self.game_window.get_width() / 2 + 70, 225))

            mouse_pos = pygame.mouse.get_pos()
            back_button = create_button(
                position=(self.game_window.get_width() / 2, 600),
                text='BACK',
                font_size=SELECTION_FONT_SIZE,
            )
            back_button.change_color(mouse_pos)
            back_button.update(self.game_window)

            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    self.end_game()
                    sys.exit()

                if event.type == pygame.constants.KEYDOWN and event.key == pygame.constants.K_ESCAPE:
                    self.end_game()

                if event.type == pygame.constants.MOUSEBUTTONDOWN:
                    if back_button.check_for_input(mouse_pos):
                        self.end_game()

            pygame.display.update()

    def display_info(self) -> None:
        left_pos = self.game_window.get_width() / 2 + 320
        right_pos = self.game_window.get_width() / 2 + 385
        top_pos = 100
        interval = 30
        gp_name = ''

        if self.settings.selected_track_name == 'TRACK 1':
            gp_name = 'HUNGARIAN GP'
        elif self.settings.selected_track_name == 'TRACK 2':
            gp_name = 'ITALIAN GP'
        elif self.settings.selected_track_name == 'TRACK 3':
            gp_name = 'BRAZILIAN GP'

        create_text(
            self.game_window,
            SECONDARY_FONT_SIZE,
            gp_name,
            position=(right_pos, top_pos - 50),
            positioning='midright'
        )
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
            position=(self.game_window.get_width() / 2, self.game_window.get_height() / 2)
        )

    def display_wrong_way_text(self) -> None:
        create_text(
            self.game_window,
            SECONDARY_FONT_SIZE,
            'WRONG WAY',
            color='#b68f40',
            position=(self.game_window.get_width() / 2, self.game_window.get_height() / 2)
        )

    def determine_penalty(self, track_name: str, time_out_of_track: float = 0.0) -> None:
        if self.settings.penalties == 'ON':
            if self.player.corner_cut(COLLISION_POINTS[track_name]):
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
            position=(self.game_window.get_width() / 2, 300)
        )
        self.game_window.blit(FLAG_PENALTY, (self.game_window.get_width() / 2 + 125, 265))

    def create_results_texts(self) -> None:
        left_pos = self.game_window.get_width() / 2 - 175
        right_pos = self.game_window.get_width() / 2 + 175
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

    def save_score(self) -> None:
        filename = 'highscores.csv'
        highscores = read_highscores_file(filename)
        size = len(highscores)

        if not size:
            highscores.append(self.create_score_data(1))
            update_highscores_file(filename, highscores)

            return

        score_inserted = False

        for i in range(size):
            if self.player.score > highscores[i][1]:
                highscores.insert(i, self.create_score_data(i + 1))
                score_inserted = True

                for j in range(i + 1, size + 1):
                    highscores[j][0] += 1

                if len(highscores) > 8:
                    highscores.pop()

                break

        if not score_inserted and size < 8:
            highscores.append(self.create_score_data(size + 1))

            score_inserted = True

        if score_inserted:
            update_highscores_file(filename, highscores)

    def create_score_data(self, place: int) ->  list[int | str]:
        return [
            place,
            self.player.score,
            self.settings.player_nickname,
            self.settings.selected_car_name,
            self.settings.selected_track_name,
            self.player.best_lap,
            self.settings.penalties
        ]