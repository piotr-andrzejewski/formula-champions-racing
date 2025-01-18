import sys

import pygame

from game import Game
from utils import Button, blit_screen, create_game_screen, get_font


class Menu:
    def __init__(self, game_window: pygame.display) -> None:
        self.game_window = game_window
        self.display_menu = True
        self.play_game = False
        self.set_options = False

    def reset(self) -> None:
        self.display_menu = True
        self.play_game = False
        self.set_options = False

    def main_menu(self) -> None:
        while self.display_menu:
            game = Game(self.game_window)
            self.game_window.fill('black')
            menu_mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(400, 200))

            play_button = Button(
                position=(400, 400),
                text_input="PLAY",
                font=get_font(75),
                base_color="#d7fcd4",
                hover_color="White"
            )
            settings_button = Button(
                position=(400, 500),
                text_input="SETTINGS",
                font=get_font(75),
                base_color="#d7fcd4",
                hover_color="White"
            )
            quit_button = Button(
                position=(400, 600),
                text_input="QUIT",
                font=get_font(75),
                base_color="#d7fcd4",
                hover_color="White"
            )

            self.game_window.blit(menu_text, menu_rect)

            for button in [play_button, settings_button, quit_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.game_window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(menu_mouse_pos):
                        blit_screen(self.game_window)
                        self.play_game = True
                        self.display_menu = False
                        game.run()
                        pygame.init()
                        self.game_window = create_game_screen(800, 800)

                    if settings_button.check_for_input(menu_mouse_pos):
                        self.set_options = True
                        self.display_menu = False

                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

        self.reset()