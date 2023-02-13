import pygame


class Worm:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.direction = "right"
        self.length = 1
        self.body = (x, y)
        self.alive = True

    def draw(self):
        pygame.draw.circle(self.player.game.window,
                           self.player.color,
                           (self.x, self.y), 5)
