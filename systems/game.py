import sys

from systems.settings import Settings
import pygame

class Game:
    def __init__(self):
        self.settings = Settings()

        pygame.init()

        # create the window according to settings width, height, fullscreen
        self.window = pygame.display.set_mode((self.settings.width, self.settings.height), pygame.FULLSCREEN if self.settings.fullscreen else 0)

        pygame.display.set_caption(self.settings.title)


    def close(self):
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                sys.exit()

    def update(self):
        pass

    def draw(self):
        pass

