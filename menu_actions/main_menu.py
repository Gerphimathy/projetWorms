# Declare text, actions pairs for main menu to be loaded by game and added to main menu controller
import sys

import pygame


def main_menu_options():
    # Each name, function pair will be attributed to a menu_option object

    def play(self):
        def inner():
            self.menu.game.state = 'pregame_menu'

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

    return [('Jouer', play, None), ('Options', options, None), ('Quitter le jeu', close, None)]
