# main game

import pygame
import time

from cars import generate_player, generate_opponents
from images import CAR_1, CAR_2, CAR_3, CAR_4, CAR_5, CAR_6, CAR_7, CAR_8, CUP, FINISH_LINE, TRACK_1, TRACK_1_LIMITS
from settings import GameSettings

mili = 1000

# constants for the game
TRACK_1_POSITION = (10, 10)
TRACK_1_LIMITS_POSITION = (10, 10)
TRACK_1_FINISH_LINE_POSITION = (535, 762)

# create font for on screen messages
pygame.font.init()
GAME_FONT = pygame.font.SysFont('Space Bd BT', 36)
GAME_FONT.render('START', True, (255, 255, 255), (0, 0, 0))

# create game window
GAME_WINDOW = pygame.display.set_mode((800, 800))
GAME_WINDOW.fill((0, 50, 0))
pygame.display.set_caption('Formula Champions Racing')
pygame.display.set_icon(CUP)

# set frames per second parameter
FPS = 60
CLOCK = pygame.time.Clock()

GAME_IMAGES = [
    (TRACK_1_LIMITS, TRACK_1_LIMITS_POSITION),
    (TRACK_1, TRACK_1_POSITION),
    (FINISH_LINE, TRACK_1_FINISH_LINE_POSITION)
]

TRACK_1_LIMITS_MASK = pygame.mask.from_surface(TRACK_1_LIMITS)
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE)

# initialize required classes
SETTINGS = GameSettings()
PLAYER = generate_player()
COMPUTERS = generate_opponents()


def draw() -> None:
    for img, pos in GAME_IMAGES:
        GAME_WINDOW.blit(img, pos)

    PLAYER.draw(GAME_WINDOW)

    for computer in COMPUTERS:
        computer.draw(GAME_WINDOW)

    pygame.display.update()


def move_player() -> None:
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_w]:
        moved = True
        PLAYER.move_forward()
        if keys[pygame.K_a]:
            PLAYER.rotate(left=True)
        elif keys[pygame.K_d]:
            PLAYER.rotate(right=True)
    elif keys[pygame.K_s]:
        moved = True
        if PLAYER.vel <= 0:
            PLAYER.reverse()
            if keys[pygame.K_a]:
                PLAYER.rotate(right=True)
            elif keys[pygame.K_d]:
                PLAYER.rotate(left=True)
        else:
            PLAYER.brake()
            if keys[pygame.K_a]:
                PLAYER.rotate(left=True)
            elif keys[pygame.K_d]:
                PLAYER.rotate(right=True)

    if not moved:
        PLAYER.reduce_speed()
        if PLAYER.vel != 0:
            if keys[pygame.K_a]:
                PLAYER.rotate(left=True)
            elif keys[pygame.K_d]:
                PLAYER.rotate(right=True)


def handle_collisions() -> None:
    # TODO: handle track limits for potential penalties when player turns on such option
    if PLAYER.collide(TRACK_1_LIMITS_MASK, *TRACK_1_LIMITS_POSITION) is None:
        print("Get back to track")


def handle_finish_line_crossing() -> None:
    for computer in COMPUTERS:
        computer_finish_line_poi = computer.collide(FINISH_LINE_MASK, *TRACK_1_FINISH_LINE_POSITION)

        if computer_finish_line_poi is not None:
            computer.crossed_line = True
            computer.current_point = 0

        if computer_finish_line_poi is None:
            if computer.crossed_line:
                computer.completed_laps += 1
                computer.crossed_line = False

    player_finish_line_poi = PLAYER.collide(FINISH_LINE_MASK, *TRACK_1_FINISH_LINE_POSITION)

    if player_finish_line_poi is not None:
        if player_finish_line_poi[0] > 0:
            PLAYER.crossed_line = True

        if not PLAYER.crossed_line:
            print("Wrong way")
            PLAYER.reset_position()

    if player_finish_line_poi is None:
        if PLAYER.crossed_line:
            current_time = time.time_ns() / mili
            PLAYER.completed_laps += 1
            PLAYER.lap_times.append(round(current_time - PLAYER.lap_start_time))
            PLAYER.lap_start_time = current_time
            PLAYER.crossed_line = False
            print("Lap completed")


def generate_path_for_computer_car() -> None:
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        # code to generate points for computer car path
        if event.type == pygame.KEYDOWN:
            if pressed_keys[pygame.K_x]:
                # display player position to better tune computer car's path
                print((PLAYER.x, PLAYER.y))

        # code to get coordinates of mouse position
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos)

        # select index of computer car for which you want to create path
        i = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            COMPUTERS[i].path.append(mouse_pos)

        # code to delete last path point
        if event.type == pygame.KEYDOWN:
            if pressed_keys[pygame.K_c]:
                COMPUTERS[i].path.pop()

        # code to add many points from player's position
        if pressed_keys[pygame.K_SPACE]:
            COMPUTERS[i].path.append((PLAYER.x, PLAYER.y))


def get_best_lap() -> None:
    PLAYER.find_best_lap()
    if PLAYER.best_lap is not None:
        print(f"Best lap: {PLAYER.best_lap}")

class Game:
    def __init__(self) -> None:
        self.game_started = False
        self.game_start_time = 0.0

    def reset(self) -> None:
        self.game_started = False
        self.game_start_time = 0.0
        PLAYER.score = 0
        PLAYER.final_position = 1
        PLAYER.lap_start_time = 0.0
        PLAYER.lap_times = []

    def start_game(self) -> None:
        self.game_started = True
        self.game_start_time = time.time_ns() / mili

    def get_total_time(self) -> float:
        if not self.game_started:
            return 0

        return round(time.time_ns() / mili - self.game_start_time)

    def run(self) -> None:
        self.start_game()
        # main event loop for the game
        while self.game_started:
            # set max fps for the game
            CLOCK.tick(FPS)

            for event in pygame.event.get():
                # check the event of user clicking 'X' button to close the game window
                if event.type == pygame.QUIT:
                    self.game_started = False

            draw()
            move_player()
            # generate_path_for_computer_car()

            handle_collisions()
            handle_finish_line_crossing()

            if PLAYER.completed_laps == SETTINGS.selected_laps:
                self.game_started = False

        print("Laps completed:")
        print("Player: ", PLAYER.completed_laps)

        for i in range(len(COMPUTERS)):
            print(f"Computer_{i + 1}: ", COMPUTERS[i].completed_laps)
            # # code to display computer car's path in console to be able to copy it for PATH variable
            # print(computers[i].path)

        print(f"Total time: {self.get_total_time()}")
        get_best_lap()


        pygame.quit()

