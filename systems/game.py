import sys

from systems.settings import Settings
import pygame

from controllers.menu import Menu

from menu_actions.main_menu import main_menu_options, main_menu_style


class Game:
    def __init__(self):
        self.settings = Settings()

        pygame.init()

        # create the window according to settings width, height, fullscreen, fps
        self.window = pygame.display.set_mode((self.settings.width, self.settings.height),
                                              pygame.FULLSCREEN if self.settings.fullscreen else 0)
        pygame.display.set_caption(self.settings.title)

        # set the fps
        self.clock = pygame.time.Clock()
        self.clock.tick(self.settings.fps)

        self.states = {
            "main_menu": Menu("Menu Principal", self, main_menu_options(), main_menu_style()),
            "game": None,
            "pause_menu": None,
            "settings_menu": None,
        }
        self.__state = "main_menu"

        self.draw()

    def __get_state(self):
        return self.states[self.__state]

    def __set_state(self, value):
        if value in self.states:
            self.__state = value
            self.update()
        else:
            raise ValueError("Invalid state")

    state = property(__get_state, __set_state)

    def close(self):
        pygame.quit()

    def events(self):
        for event in pygame.event.get():

            # close events take priority
            if event.type == pygame.QUIT:
                self.close()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                self.close()
                sys.exit()
            else:
                self.state.event(event)

    def update(self):
        pass

    def draw(self):
        self.state.draw(self.window)
