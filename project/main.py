# main game
import time

import pygame

from pygame import Surface

from cars import ComputerCar, PlayerCar
from images import CAR_2, CUP, FINISH_LINE, TRACK_1, TRACK_1_LIMITS, CAR_3, CAR_4, CAR_5, CAR_6, CAR_7, CAR_8

# create font for on screen messages
pygame.font.init()
GAME_FONT = pygame.font.SysFont('Space Bd BT', 36)

# create game window
GAME_WINDOW = pygame.display.set_mode((800, 800))
GAME_WINDOW.fill((0, 50, 0))
pygame.display.set_caption('Formula Champions Racing')
pygame.display.set_icon(CUP)
GAME_FONT.render('START', True, (255, 255, 255), (0, 0, 0))


def draw(
        window: pygame.display,
        images: list[tuple[Surface, (int, int)]],
        player_car: PlayerCar,
        computer_cars: list[ComputerCar]
) -> None:
    for img, pos in images:
        window.blit(img, pos)

    player_car.draw(window)

    for computer_car in computer_cars:
        computer_car.draw(window)

    pygame.display.update()


def move_player(player_car: PlayerCar) -> None:
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
        if keys[pygame.K_a]:
            player_car.rotate(left=True)
        elif keys[pygame.K_d]:
            player_car.rotate(right=True)
    elif keys[pygame.K_s]:
        moved = True
        if player_car.vel <= 0:
            player_car.reverse()
            if keys[pygame.K_a]:
                player_car.rotate(right=True)
            elif keys[pygame.K_d]:
                player_car.rotate(left=True)
        else:
            player_car.brake()
            if keys[pygame.K_a]:
                player_car.rotate(left=True)
            elif keys[pygame.K_d]:
                player_car.rotate(right=True)

    if not moved:
        player_car.reduce_speed()
        if player.vel != 0:
            if keys[pygame.K_a]:
                player.rotate(left=True)
            elif keys[pygame.K_d]:
                player.rotate(right=True)


def check_events(player_car: PlayerCar, computer_cars: list[ComputerCar]) -> bool:
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        # check the event of user clicking 'X' button to close the game window
        if event.type == pygame.QUIT:
            return False

        # code to generate points for computer car path
        if event.type == pygame.KEYDOWN:
            if pressed_keys[pygame.K_x]:
                # display player position to better tune computer car's path
                print((player_car.x, player_car.y))

        # code to get coordinates of mouse position
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos)

        # select index of computer car for which you want to create path
        i = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            computer_cars[i].path.append(mouse_pos)

        # code to delete last path point
        if event.type == pygame.KEYDOWN:
            if pressed_keys[pygame.K_c]:
                computer_cars[i].path.pop()

        # code to add many points from player's position
        if pressed_keys[pygame.K_SPACE]:
            computer_cars[i].path.append((player_car.x, player_car.y))

    return True

# set frames per second parameter
FPS = 60
clock = pygame.time.Clock()

TRACK_1_POSITION = (10, 10)
TRACK_1_LIMITS_POSITION = (10, 10)
FINISH_LINE_POSITION = (535, 762)

game_images = [
    (TRACK_1_LIMITS, TRACK_1_LIMITS_POSITION),
    (TRACK_1, TRACK_1_POSITION),
    (FINISH_LINE, FINISH_LINE_POSITION)
]

track_1_limits_mask = pygame.mask.from_surface(TRACK_1_LIMITS)
finish_line_mask = pygame.mask.from_surface(FINISH_LINE)

TRACK_1_P1 = (380, 772)
TRACK_1_P2 = (400, 758.5)
TRACK_1_P3 = (420, 772)
TRACK_1_P4 = (440, 758.5)
TRACK_1_P5 = (460, 772)
TRACK_1_P6 = (480, 758.5)
TRACK_1_P7 = (500, 772)
TRACK_1_P8 = (520, 758.5)

player = PlayerCar(start_pos=TRACK_1_P1)
computers = [
    ComputerCar(img=CAR_2, start_pos=TRACK_1_P2),
    ComputerCar(img=CAR_3, start_pos=TRACK_1_P3),
    ComputerCar(img=CAR_4, start_pos=TRACK_1_P4),
    ComputerCar(img=CAR_5, start_pos=TRACK_1_P5),
    ComputerCar(img=CAR_6, start_pos=TRACK_1_P6),
    ComputerCar(img=CAR_7, start_pos=TRACK_1_P7),
    ComputerCar(img=CAR_8, start_pos=TRACK_1_P8)
]

start = True


def handle_collisions(player_car: PlayerCar) -> None:
    # TODO: handle track limits for potential penalties when player turns on such option
    if player_car.collide(track_1_limits_mask, *TRACK_1_LIMITS_POSITION) is None:
        print("get back to track")


def handle_finish_line_crossing(player_car: PlayerCar, computer_cars: list[ComputerCar]) -> None:

    for computer_car in computer_cars:
        computer_car_finish_line_poi = computer_car.collide(finish_line_mask, *FINISH_LINE_POSITION)

        if computer_car_finish_line_poi is not None:
            computer_car.crossed_line = True
            computer_car.current_point = 0

        if computer_car_finish_line_poi is None:
            if computer_car.crossed_line:
                computer_car.completed_laps += 1
                computer_car.crossed_line = False

    player_car_finish_line_poi = player_car.collide(finish_line_mask, *FINISH_LINE_POSITION)

    if player_car_finish_line_poi is not None:
        if player_car_finish_line_poi[0] > 0:
            player_car.crossed_line = True

        if not player.crossed_line:
            print("wrong way")
            player_car.reset_position()

    if player_car_finish_line_poi is None:
        if player_car.crossed_line:
            player_car.completed_laps += 1
            player_car.crossed_line = False
            print("Lap completed")


def run_game(run: bool, player_car: PlayerCar, computer_cars: list[ComputerCar]) -> None:
    # main event loop for the game
    while run:
        # set max fps for the game
        clock.tick(FPS)

        draw(GAME_WINDOW, game_images, player_car, computer_cars)
        run = check_events(player_car, computer_cars)
        move_player(player_car)

        # for computer_car in computer_cars:
        #     computer_car.move()

        handle_collisions(player_car)
        handle_finish_line_crossing(player_car, computer_cars)

    print("Laps completed:")
    print("Player: ", player_car.completed_laps)

    for i in range(len(computer_cars)):
        print(f"Computer_{i + 1}: ", computer_cars[i].completed_laps)
        # # code to display computer car's path in console to be able to copy it for PATH variable
        # print(computer_car.path)

    pygame.quit()


run_game(start, player, computers)