import pygame

from systems.settings import Settings


def settings_options(game):
    def back(self):
        def inner():
            self.menu.game.state = "main_menu"

        return inner

    def resolution(self):
        def inner():
            value = self.get_current_value()
            self.menu.game.settings.width = value[0]
            self.menu.game.settings.height = value[1]
            self.menu.game.window = pygame.display.set_mode(
                (self.menu.game.settings.width, self.menu.game.settings.height))

        return inner

    current_res = (game.settings.width, game.settings.height)
    # 2 dimensional array: game.settings.possibleValues['width'], game.settings.possibleValues['height']
    possible_res = [(width, height) for width in game.settings.possibleValues['width'] for height in game.settings.possibleValues['height']]

    return [('Retour', back, None), ('Résolution', resolution, "lateral", possible_res, current_res)]
