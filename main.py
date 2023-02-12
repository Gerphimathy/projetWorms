import pygame

from systems.game import Game

# run the game
game = Game()

while True:
    game.events()
    pygame.display.update()
