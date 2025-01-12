# utility functions

import pygame

from pygame import Surface

def scale_image(img: Surface, factor: float) -> Surface:
    new_size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, new_size)


def blit_rotate_center(window: pygame.display, img: Surface, top_left: tuple[int, int], angle: float) -> None:
    rotated_image = pygame.transform.rotate(img, angle)
    new_rect = rotated_image.get_rect(center=img.get_rect(topleft=top_left).center)
    window.blit(rotated_image, new_rect.topleft)