import pygame

from systems.game import Game

# run the game
game = Game()

while True:
    game.update()
    pygame.display.update()
