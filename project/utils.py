# utility functions

import pygame

from pygame import Surface

pygame.font.init()


def scale_image(img: Surface, factor: float = 1) -> Surface:
    new_size = round(img.get_width() * factor), round(img.get_height() * factor)

    return pygame.transform.scale(img, new_size)


def blit_rotate_center(window: Surface, img: Surface, top_left: tuple[float, float], angle: float) -> None:
    rotated_image = pygame.transform.rotate(img, angle)
    new_rect = rotated_image.get_rect(center=img.get_rect(topleft=top_left).center)
    window.blit(rotated_image, new_rect.topleft)


def blit_text_center(window: Surface, font: pygame.font, text: str) -> None:
    render = font.render(text, 1, (200, 200, 200))
    window.blit(
        render,
        (window.get_width() / 2 - render.get_width() / 2, window.get_height() / 2 - render.get_height() / 2)
    )

def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font('./assets/Space_Bd_BT_Bold.ttf', size)


def blit_screen(window: Surface):
    window.blit(Surface((window.get_width(), window.get_height())), (0, 0))
    pygame.display.update()


def create_game_screen(width: int, height: int) -> Surface:
    game_screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Formula Champions Racing')
    pygame.display.set_icon(pygame.image.load('./assets/cup.png'))

    return game_screen


# def get_pressed_keys() -> ScancodeWrapper:
#     return pygame.key.get_pressed()


class Button:
    def __init__(
            self,
            text_input: str,
            position: tuple[int, int],
            font: pygame.font.Font,
            base_color: str,
            hover_color: str,
    ) -> None:
        self.text_input = text_input
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen: Surface) -> None:
        screen.blit(self.text, self.rect)

    def check_for_input(self, position: tuple[int, int]) -> bool:
        if (position[0] in range(self.rect.left, self.rect.right)
                and position[1] in range(self.rect.top, self.rect.bottom)):
            return True

        return False

    def change_color(self, position: tuple[int, int]) -> None:
        if (position[0] in range(self.rect.left, self.rect.right)
                and position[1] in range(self.rect.top, self.rect.bottom)):
            self.text = self.font.render(self.text_input, True, self.hover_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
