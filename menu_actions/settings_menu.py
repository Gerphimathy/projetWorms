import pygame


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

    def fullscreen(self):
        def inner():
            value = self.get_current_value()
            self.menu.game.settings.fullscreen = value
            self.menu.game.window = pygame.display.set_mode(
                (self.menu.game.settings.width, self.menu.game.settings.height), pygame.FULLSCREEN if value else 0)

        return inner

    return [('Retour', back, None),

            ('Résolution', resolution, "lateral",
            [(width, height) for width in game.settings.possibleValues['width']
             for height in game.settings.possibleValues['height']],
             (game.settings.width, game.settings.height)),

            ('Plein écran', fullscreen, "lateral",
             game.settings.possibleValues['fullscreen'], game.settings.fullscreen),
            ]
