import sys

from systems.settings import Settings
import pygame

from controllers.menu import Menu
from controllers.partie import Partie

from menu_actions.main_menu import main_menu_options

from menu_actions.menu_style import default_menu_style

from menu_actions.settings_menu import settings_options

from menu_actions.pregame_menu import pregame_menu_options

from menu_actions.weapons_menu import weapons_options


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
            "main_menu": Menu("Menu Principal", self, main_menu_options(), default_menu_style()),
            "pregame_menu": Menu("Préparation de la partie", self, pregame_menu_options(), default_menu_style()),
            "game": Partie(None, 0, 0, "flat"),
            "weapons_menu": Menu("Armes", self, weapons_options(), default_menu_style()),
            "settings_menu": Menu("Options", self, settings_options(self), default_menu_style()),
        }
        self.__state = "main_menu"

        self.draw()

    def __get_state(self):
        return self.states[self.__state]

    def __set_state(self, value):
        if value in self.states:
            previous_state = self.__state
            self.__state = value
            self.update_state(previous_state)
        else:
            raise ValueError("Invalid state")

    state = property(__get_state, __set_state)

    def close(self):
        pygame.quit()

    def events(self):

        # print(self.clock.get_fps())
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

    def update_state(self, previous_state):
        if previous_state == "pregame_menu" and self.__state == "game":
            data = self.states[previous_state].data
            self.states["game"] = Partie(self, data["player_count"], data["worms_per_player"], data["map_type"])
        else:
            self.state.draw(self.window)

    def update(self):
        self.clock.tick(self.settings.fps)
        self.events()
        self.state.update()

    def draw(self):
        self.state.draw(self.window)
