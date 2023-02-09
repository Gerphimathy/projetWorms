from systems.game import Game

# run the game
game = Game()

while True:
    game.events()
    game.update()
    game.draw()

