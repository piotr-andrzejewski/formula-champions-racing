# load images for the game

import pygame

from utils import scale_image

TRACK_1 = scale_image(pygame.image.load('./assets/track1.png'), 1.3)
TRACK_1_LIMITS = scale_image(pygame.image.load('./assets/track1_limits.png'), 1.3)
TRACK_1_TILE = scale_image(pygame.image.load('./assets/track1_tile.png'), 0.4)
TRACK_BRAZIL_TILE = pygame.image.load('./assets/track_brazil_tile.png')
TRACK_BRAZIL = pygame.image.load('./assets/track_brazil.png')
TRACK_LIMITS_BRAZIL = pygame.image.load('./assets/track_brazil_limits.png')
TRACK_ITALY_TILE = pygame.image.load('./assets/track_italy_tile.png')
TRACK_ITALY = pygame.image.load('./assets/track_italy.png')
TRACK_LIMITS_ITALY = pygame.image.load('./assets/track_italy_limits.png')


CAR_1 = pygame.image.load('./assets/car1.png')
CAR_2 = pygame.image.load('./assets/car2.png')
CAR_3 = pygame.image.load('./assets/car3.png')
CAR_4 = pygame.image.load('./assets/car4.png')
CAR_5 = pygame.image.load('./assets/car5.png')
CAR_6 = pygame.image.load('./assets/car6.png')
CAR_7 = pygame.image.load('./assets/car7.png')
CAR_8 = pygame.image.load('./assets/car8.png')

FLAG_FINISH = pygame.image.load('./assets/flag_finish.png')
FLAG_PENALTY = pygame.image.load('./assets/flag_penalty.png')

CUP = pygame.image.load('./assets/cup.png')

LIGHTS_ON_1 = pygame.image.load('./assets/lights_on_1.png')
LIGHTS_ON_2 = pygame.image.load('./assets/lights_on_2.png')
LIGHTS_ON_3 = pygame.image.load('./assets/lights_on_3.png')
LIGHTS_ON_4 = pygame.image.load('./assets/lights_on_4.png')
LIGHTS_ON_5 = pygame.image.load('./assets/lights_on_5.png')
LIGHTS_OUT = pygame.image.load('./assets/lights_out.png')

FINISH_LINE = scale_image(pygame.image.load('assets/finish_line.png'), 1.2)