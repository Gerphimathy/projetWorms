# Declare text, actions pairs for main menu to be loaded by game and added to main menu controller
import sys

import pygame


def main_menu_options():
    # Each name, function pair will be attributed to a menu_option object

    def play(self):
        def inner():
            self.menu.game.state = 'game'
        return inner

    def options(self):
        def inner():
            self.menu.game.state = "settings_menu"
        return inner

    def close(self):
        def inner():
            pygame.quit()
            sys.exit()
        return inner

    return [('Jouer', play), ('Options', options), ('Quitter le jeu', close)]


def main_menu_style():
    # pygame display style

    # IMPORTANT: Font must be BELOW background, otherwise the background will cover the font
    return {
        'background_color': (120, 120, 120),
        'background_image': None,
        'font': pygame.font.Font('assets/fonts/arial.ttf', 30),
        'font_color': (0, 0, 0),
        'font_selected_color': (255, 0, 0),
    }
