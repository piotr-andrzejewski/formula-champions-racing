# load images for the game

import pygame

from utils import scale_image

TRACK_1 = scale_image(pygame.image.load('./assets/track1.png'), 1)
TRACK_1_LIMITS = scale_image(pygame.image.load('./assets/track1_limits.png'), 1)
TRACK_1_TILE = pygame.image.load('./assets/track1_tile.png')
TRACK_2 = pygame.image.load('./assets/track2.png')
TRACK_2_LIMITS = pygame.image.load('./assets/track2_limits.png')
TRACK_2_TILE = pygame.image.load('./assets/track2_tile.png')
TRACK_3 = pygame.image.load('./assets/track3.png')
TRACK_3_LIMITS = pygame.image.load('./assets/track3_limits.png')
TRACK_3_TILE = pygame.image.load('./assets/track3_tile.png')

CAR_1 = pygame.image.load('./assets/car1.png')
CAR_1_BIG = pygame.image.load('./assets/car1_big.png')
CAR_2 = pygame.image.load('./assets/car2.png')
CAR_2_BIG = pygame.image.load('./assets/car2_big.png')
CAR_3 = pygame.image.load('./assets/car3.png')
CAR_3_BIG = pygame.image.load('./assets/car3_big.png')
CAR_4 = pygame.image.load('./assets/car4.png')
CAR_4_BIG = pygame.image.load('./assets/car4_big.png')
CAR_5 = pygame.image.load('./assets/car5.png')
CAR_5_BIG = pygame.image.load('./assets/car5_big.png')
CAR_6 = pygame.image.load('./assets/car6.png')
CAR_6_BIG = pygame.image.load('./assets/car6_big.png')
CAR_7 = pygame.image.load('./assets/car7.png')
CAR_7_BIG = pygame.image.load('./assets/car7_big.png')
CAR_8 = pygame.image.load('./assets/car8.png')
CAR_8_BIG = pygame.image.load('./assets/car8_big.png')

FLAG_FINISH = scale_image(pygame.image.load('./assets/flag_finish.png'), 0.8)
FLAG_PENALTY = scale_image(pygame.image.load('./assets/flag_penalty.png'), 0.8)

CUP = pygame.image.load('./assets/cup.png')

LIGHTS = {
    0: scale_image(pygame.image.load('./assets/lights_out.png'), 1.5),
    1: scale_image(pygame.image.load('./assets/lights_on_1.png'), 1.5),
    2: scale_image(pygame.image.load('./assets/lights_on_2.png'), 1.5),
    3: scale_image(pygame.image.load('./assets/lights_on_3.png'), 1.5),
    4: scale_image(pygame.image.load('./assets/lights_on_4.png'), 1.5),
    5: scale_image(pygame.image.load('./assets/lights_on_5.png'), 1.5),
}

FINISH_LINE = scale_image(pygame.image.load('assets/finish_line.png'), 1.2)