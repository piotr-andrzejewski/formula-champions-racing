# main game
import time

import pygame

from pygame import Surface

from cars import ComputerCar, PlayerCar
from images import CAR_2, CUP, FINISH_LINE, TRACK_1, TRACK_1_LIMITS

# create font for on screen messages
pygame.font.init()
GAME_FONT = pygame.font.SysFont('Space Bd BT', 36)

# create game window
GAME_WINDOW = pygame.display.set_mode((800, 800))
GAME_WINDOW.fill((0, 50, 0))
pygame.display.set_caption('Formula Champions Racing')
pygame.display.set_icon(CUP)
# GAME_FONT.render('START', True, (255, 255, 255), (0, 0, 0))


def draw(window: pygame.display, images: list[tuple[Surface, (int, int)]], player: PlayerCar) -> None:
    for img, pos in images:
        window.blit(img, pos)

    player.draw(window)
    computer_car_1.draw(window)
    pygame.display.update()


def move_player(player: PlayerCar) -> None:
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_w]:
        moved = True
        player.move_forward()
        if keys[pygame.K_a]:
            player.rotate(left=True)
        elif keys[pygame.K_d]:
            player.rotate(right=True)
    elif keys[pygame.K_s]:
        moved = True
        if player.vel <= 0:
            player.reverse()
            if keys[pygame.K_a]:
                player.rotate(right=True)
            elif keys[pygame.K_d]:
                player.rotate(left=True)
        else:
            player_car.brake()
            if keys[pygame.K_a]:
                player.rotate(left=True)
            elif keys[pygame.K_d]:
                player.rotate(right=True)

    if not moved:
        player_car.reduce_speed()
        if player.vel != 0:
            if keys[pygame.K_a]:
                player.rotate(left=True)
            elif keys[pygame.K_d]:
                player.rotate(right=True)

# set frames per second parameter
FPS = 60

run = True
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

player_car = PlayerCar()
computer_car_1 = ComputerCar(max_vel=1.1, img=CAR_2)

player_completed_laps = 0
player_crossed_line = False
computer_car_1_completed_laps = 0
computer_car_1_crossed_line = False

# main event loop for the game
while run:
    # set max fps for the game
    clock.tick(FPS)

    draw(GAME_WINDOW, game_images, player_car)
    # pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        # check the event of user clicking 'X' button to close the game window
        if event.type == pygame.QUIT:
            run = False
            break

        # # code to generate points for computer car path
        # if event.type == pygame.KEYDOWN:
        #     if pressed_keys[pygame.K_x]:
        #         # display player position to better tune computer car's path
        #         print((player_car.x, player_car.y))
        #
        # # code to get coordinates of mouse position
        # mouse_pos = pygame.mouse.get_pos()
        # print(mouse_pos)
        #
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     computer_car_1.path.append(mouse_pos)
        #
        # if event.type == pygame.KEYDOWN:
        #     if pressed_keys[pygame.K_c]:
        #         computer_car_1.path.pop()

    move_player(player_car)

    # if pressed_keys[pygame.K_SPACE]:
    #     computer_car_1.path.append((player_car.x, player_car.y))

    computer_car_1.draw(GAME_WINDOW)

    # TODO: handle track limits for potential penalties when player turns on such option
    if player_car.collide(track_1_limits_mask, *TRACK_1_LIMITS_POSITION) is None:
        print("get back to track")

    computer_car_1_finish_line_poi = computer_car_1.collide(finish_line_mask, *FINISH_LINE_POSITION)

    if computer_car_1_finish_line_poi is not None:
        computer_car_1_crossed_line = True
        computer_car_1.current_point = 0

    if computer_car_1_finish_line_poi is None:
        if computer_car_1_crossed_line:
            computer_car_1_completed_laps += 1
            computer_car_1_crossed_line = False

    player_car_finish_line_poi = player_car.collide(finish_line_mask, *FINISH_LINE_POSITION)

    if player_car_finish_line_poi is not None:
        if player_car_finish_line_poi[0] > 0:
                player_crossed_line = True

        if not player_crossed_line:
            print("wrong way")
            player_car.reset()

    if player_car_finish_line_poi is None:
        if player_crossed_line:
            player_completed_laps += 1
            player_crossed_line = False
            print("Lap completed")

print("Laps completed:")
print("Player: ", player_completed_laps)
print("Computer_1: ", computer_car_1_completed_laps)

# code to display computer car's path in console to be able to copy it for PATH variable
# print(computer_car_1.path)

pygame.quit()
