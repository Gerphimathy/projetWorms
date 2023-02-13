from entities.worm import Worm


class Player:
    def __init__(self, color, nb_worms, game):
        self.color = color
        self.worms = [Worm(0, 0, self) for _ in range(nb_worms)]
        self.alive = True
        self.game = game
