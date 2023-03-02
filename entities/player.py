import pygame.sprite

from entities.worm import Worm


class Player:
    def __init__(self, color, nb_worms, game, sprites_groups):
        self.color = color
        self.player_sprites = pygame.sprite.Group()
        self.worms = [Worm(0, 0, self, sprites_groups) for _ in range(nb_worms)]
        self.alive = True
        self.game = game
        self.next_worm_generator = self.get_next_worm()

    def get_next_worm(self):
        while True:
            for worm in self.worms:
                if worm.alive:
                    worm.active = True
                    yield worm
                    worm.active = False

