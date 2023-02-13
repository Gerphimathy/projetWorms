import sys

from systems.settings import Settings
import pygame

from controllers.menu import Menu
from controllers.partie import Partie

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
            "game": Partie(0, 0, None),
            "pause_menu": None,
            "settings_menu": None,
        }
        self.__state = "main_menu"

        self.draw()

    def __get_state(self):
        return self.states[self.__state]

    def __set_state(self, value):
        if value in self.states:
            previous_state = self.__state
            self.__state = value
            self.update(previous_state)
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
                self.state.events(event)

    def update(self, previous_state):
        if previous_state == "main_menu" and self.__state == "game":
            # Todo, set players from main menu
            # Todo, Implement choose a number, then reuse it for settings
            # Todo, Implement loading screen before terrain generation
            self.states["game"] = Partie(4, 4, self)

    def draw(self):
        self.state.draw(self.window)
