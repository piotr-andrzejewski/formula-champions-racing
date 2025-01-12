# main game

import pygame

from pygame import Surface

from cars import PlayerCar
from images import CUP, TRACK_HUNGARY
from utils import scale_image


# create game window
GAME_WINDOW = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Formula Champions Racing')
pygame.display.set_icon(CUP)


def draw(window: pygame.display, images: list[tuple[Surface, (int, int)]], player: PlayerCar) -> None:
    for img, pos in images:
        window.blit(img, pos)

    player.draw(window)
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
hungary_track = [(scale_image(TRACK_HUNGARY, 0.2), (-40, -20))]
player_car = PlayerCar(2.5, 2.3)

# main event loop for the game
while run:
    # set max fps for the game
    clock.tick(FPS)

    draw(GAME_WINDOW, hungary_track, player_car)

    for event in pygame.event.get():
        # check the event of user clicking 'X' button to close the game window
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)

pygame.quit()
