import pygame.sprite

from entities.worm import Worm


class Player:
    def __init__(self, color, nb_worms, game, partie, sprites_groups):
        self.color = color
        self.player_sprites = pygame.sprite.Group()
        self.game = game
        self.partie = partie
        self.worms = [Worm(0, 0, self, sprites_groups, self.partie) for _ in range(nb_worms)]
        self.alive = True
        self.next_worm_generator = self.get_next_worm()

    def get_next_worm(self):
        while True:
            for worm in self.worms:
                if worm.alive:
                    yield worm

    def update(self):
        if len(self.worms) < 1:
            self.alive = False
            self.partie.players.remove(self)
        else:
            for worm in self.worms:
                worm.update()
