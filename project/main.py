from menu import Menu
from utils import create_game_screen

# create game window
GAME_WINDOW = create_game_screen(800, 800)

game_menu = Menu(GAME_WINDOW)

while game_menu.display_menu:
    game_menu.main_menu()