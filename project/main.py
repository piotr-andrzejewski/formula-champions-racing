# main game

import pygame

from pygame import Surface

from cars import ComputerCar, PlayerCar
from images import CAR_2, CUP, FINISH_LINE, TRACK_HUNGARY, TRACK_LIMITS_HUNGARY


# create game window
GAME_WINDOW = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Formula Champions Racing')
pygame.display.set_icon(CUP)


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

# TODO: update PATH for better experience
PATH = [
(350, 762), (329, 762), (284, 764), (206, 763), (122, 764), (82, 757), (66, 738), (95, 700), (171, 667), (260, 663), (332, 659), (366, 645), (373, 618), (314, 575), (282, 535), (269, 490), (248, 425), (225, 314), (222, 260), (207, 214), (156, 166), (102, 117), (98, 80), (165, 52), (250, 50), (318, 76), (345, 118), (416, 165), (481, 142), (541, 159), (580, 222), (658, 280), (726, 319), (726, 415), (723, 542), (712, 610), (626, 610), (536, 620), (562, 661), (675, 674), (686, 748), (598, 761), (466, 759), (404, 758)
# (185, 760), (66, 750), (91, 683), (250, 658), (364, 651), (358, 594), (265, 510), (226, 292), (192, 192), (98, 120), (142, 57), (272, 58), (389, 154), (478, 149), (569, 200), (661, 285), (730, 386), (721, 562), (688, 617), (569, 610), (569, 659), (677, 666), (674, 750), (514, 766), (341, 760)
]

run = True
clock = pygame.time.Clock()

TRACK_HUNGARY_POSITION = (-40, -20)
TRACK_LIMITS_HUNGARY_POSITION = (5, 1)
FINISH_LINE_POSITION = (508, 748)

game_images = [
    (TRACK_HUNGARY, TRACK_HUNGARY_POSITION),
    (TRACK_LIMITS_HUNGARY, TRACK_LIMITS_HUNGARY_POSITION),
    (FINISH_LINE, FINISH_LINE_POSITION)
]

track_limits_hungary_mask = pygame.mask.from_surface(TRACK_LIMITS_HUNGARY)
finish_line_mask = pygame.mask.from_surface(FINISH_LINE)

player_car = PlayerCar()
computer_car_1 = ComputerCar(max_vel=2.0, rotation_vel=6.0, img=CAR_2, path=PATH)

player_completed_laps = 0
player_crossed_line = False
computer_car_1_completed_laps = 0
computer_car_1_crossed_line = False


# main event loop for the game
while run:
    # set max fps for the game
    clock.tick(FPS)

    draw(GAME_WINDOW, game_images, player_car)

    for event in pygame.event.get():
        # check the event of user clicking 'X' button to close the game window
        if event.type == pygame.QUIT:
            run = False
            break

        # code to generate points for computer car path
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     mouse_pos = pygame.mouse.get_pos()
        #     computer_car_1.path.append(mouse_pos)

    move_player(player_car)
    computer_car_1.move()

    # TODO: handle track limits for potential penalties when player turns on such option
    # if player_car.collide(track_limits_hungary_mask, *TRACK_LIMITS_HUNGARY_POSITION) is not None:
    #     print("collide")

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

    # display player position to better tune computer car's path
    # print((player_car.x, player_car.y))

print("Laps completed:")
print("Player: ", player_completed_laps)
print("Computer_1: ", computer_car_1_completed_laps)

# code to display computer car's path in console to be able to copy it for PATH variable
# print(computer_car_1.path)

pygame.quit()
