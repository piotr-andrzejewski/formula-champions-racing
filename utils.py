# utility functions

import csv
import os

import pygame.display
import pygame.draw
import pygame.font
import pygame.image
import pygame.transform
from pygame.surface import Surface

pygame.font.init()

# constants
TITLE_FONT_SIZE = 80
MAIN_FONT_SIZE = 70
SECONDARY_FONT_SIZE = 50
SELECTION_FONT_SIZE = 25
HIGHSCORE_FONT_SIZE = 20
GAME_INFO_FONT_SIZE = 15


class Button:
    def __init__(
            self,
            text_input: str,
            position: tuple[float, float],
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


def create_button(
        position: tuple[float, float],
        text: str,
        font_size: int,
        base_color: str = '#d7fcd4',
        hover_color: str = 'white'
) -> Button:
    return Button(
        position=position,
        text_input=text,
        font=get_font(font_size),
        base_color=base_color,
        hover_color=hover_color
    )


def scale_image(img: Surface, factor: float = 1) -> Surface:
    new_size = round(img.get_width() * factor), round(img.get_height() * factor)

    return pygame.transform.scale(img, new_size)


def blit_rotate_center(window: Surface, img: Surface, top_left: tuple[float, float], angle: float) -> None:
    rotated_image = pygame.transform.rotate(img, angle)
    new_rect = rotated_image.get_rect(center=img.get_rect(topleft=top_left).center)
    window.blit(rotated_image, new_rect.topleft)


def get_font(size: int) -> pygame.font.Font:
    return pygame.font.Font('./assets/Space_Bd_BT_Bold.ttf', size)


def blit_screen(window: Surface) -> None:
    window.blit(Surface((window.get_width(), window.get_height())), (0, 0))
    pygame.display.update()


def create_game_screen(width: int, height: int) -> Surface:
    game_screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Formula Champions Racing')
    pygame.display.set_icon(pygame.image.load('./assets/cup.png'))

    return game_screen


# create text positioned by its center, midleft or midright
def create_text(
        game_window: Surface,
        font_size: int = MAIN_FONT_SIZE,
        text: str = 'SAMPLE TEXT',
        color: str = '#d7fcd4',
        position: tuple[float, float] = (400, 400),
        positioning: str = 'center'
) -> None:
    text = get_font(font_size).render(text, True, color)

    if positioning == 'midleft':
        text_rect = text.get_rect(midleft=position)
    elif positioning == 'midright':
        text_rect = text.get_rect(midright=position)
    else:
        text_rect = text.get_rect(center=position)

    game_window.blit(text, text_rect)


def file_exists(filename: str) -> bool:
    if os.path.exists(filename):
        return True

    return False


def file_open_scope(filename: str) -> str:
    if not file_exists(filename):
        return 'a+'

    return 'r+'


def read_scores_file(filename: str, limit: int = 0) ->  list[list[int | str]]:
    with open(filename, file_open_scope(filename), encoding='utf-8', newline='') as file:
        reader = csv.reader(file)
        scores = []
        counter = 0

        for row in reader:
            row_place = int(row[0])
            row_score = int(row[1])
            row_nickname = row[2]
            row_car_name = row[3]
            row_track_name = row[4]
            row_best_lap = row[5]
            row_penalties = row[6]
            scores.append([
                row_place,
                row_score,
                row_nickname,
                row_car_name,
                row_track_name,
                row_best_lap,
                row_penalties
            ])
            counter += 1

            if counter == limit:
                break

    return scores


def update_scores_file(filename: str, data: list[list[int | str]]) -> None:
        with open(filename, file_open_scope(filename), encoding='utf-8', newline='') as file:
            file.truncate(0)
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(data)


# helper function to draw points of computer car's path
def draw_points(path: list[tuple[int, int]], window: Surface) -> None:
    for point in path:
        pygame.draw.circle(window, (255, 0, 0), point, 2)