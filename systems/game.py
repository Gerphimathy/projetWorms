import sys

from systems.settings import Settings
import pygame


class Game:
    def __init__(self):
        self.settings = Settings()

        pygame.init()

        # create the window according to settings width, height, fullscreen, fps
        self.window = pygame.display.set_mode((self.settings.width, self.settings.height), pygame.FULLSCREEN if self.settings.fullscreen else 0)
        pygame.display.set_caption(self.settings.title)

        # set the fps
        self.clock = pygame.time.Clock()
        self.clock.tick(self.settings.fps)


        # TODO: create controller classes for each system
        # One controller for menus, one for the game
        # we can use the same controller for the main menu, pause menu, etc.
        self.states = {
            "main_menu": None,
            "game": None,
            "pause_menu": None,
            "settings_menu": None,
        }
        self.state = "main_menu"

    def close(self):
        pygame.quit()

    def events(self):
        for event in pygame.event.get():

            # close events take priority
            if event.type == pygame.QUIT:
                self.close()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.close()
                    sys.exit()
            else:
                pass
                # TODO: Lets the current state's controller handle the event
                # self.states[self.state].events(event)

    def update(self):
        pass

    def draw(self):
        pass
