# load images for the game

import pygame

from utils import scale_image

TRACK_BRAZIL_TILE = pygame.image.load('./assets/track_brazil_tile.png')
TRACK_BRAZIL = pygame.image.load('./assets/track_brazil.png')
TRACK_LIMITS_BRAZIL = pygame.image.load('./assets/track_brazil_limits.png')
TRACK_HUNGARY_TILE = pygame.image.load('./assets/track_hungary_tile.png')
TRACK_HUNGARY = scale_image(pygame.image.load('./assets/track_hungary.png'), 0.2)
TRACK_LIMITS_HUNGARY = scale_image(pygame.image.load('./assets/track_hungary_limits.png'), 0.2)
TRACK_ITALY_TILE = pygame.image.load('./assets/track_italy_tile.png')
TRACK_ITALY = pygame.image.load('./assets/track_italy.png')
TRACK_LIMITS_ITALY = pygame.image.load('./assets/track_italy_limits.png')

CAR_1 = scale_image(pygame.image.load('./assets/car1.png'), 0.02)
CAR_2 = scale_image(pygame.image.load('./assets/car2.png'), 0.02)
CAR_3 = scale_image(pygame.image.load('./assets/car3.png'), 0.02)
CAR_4 = scale_image(pygame.image.load('./assets/car4.png'), 0.02)
CAR_5 = scale_image(pygame.image.load('./assets/car5.png'), 0.02)
CAR_6 = scale_image(pygame.image.load('./assets/car6.png'), 0.02)
CAR_7 = scale_image(pygame.image.load('./assets/car7.png'), 0.02)
CAR_8 = scale_image(pygame.image.load('./assets/car8.png'), 0.02)

FLAG_FINISH = pygame.image.load('./assets/flag_finish.png')
FLAG_PENALTY = pygame.image.load('./assets/flag_penalty.png')

CUP = pygame.image.load('./assets/cup.png')

LIGHTS_ON_1 = pygame.image.load('./assets/lights_on_1.png')
LIGHTS_ON_2 = pygame.image.load('./assets/lights_on_2.png')
LIGHTS_ON_3 = pygame.image.load('./assets/lights_on_3.png')
LIGHTS_ON_4 = pygame.image.load('./assets/lights_on_4.png')
LIGHTS_ON_5 = pygame.image.load('./assets/lights_on_5.png')
LIGHTS_OUT = pygame.image.load('./assets/lights_out.png')

FINISH_LINE = scale_image(pygame.image.load('assets/finish.png'), 0.02)