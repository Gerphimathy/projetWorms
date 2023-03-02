from random import random

import pygame

import systems.terrain

from entities.worm import Worm
from entities.player import Player


class Partie:
    def __init__(self, game, players, w_p_player, terrain_type):
        if game is None:
            return

        self.game = game

        self.all_sprites = pygame.sprite.Group()
        self.all_players_sprites = pygame.sprite.Group()

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.players = [Player(colors[_], w_p_player, self.game, [self.all_sprites, self.all_players_sprites]) for _ in
                        range(players)]

        self.dimensions = (game.settings.width, game.settings.height)
        self.terrain_type = terrain_type
        self.worm_per_player = w_p_player
        self.terrain = systems.terrain.generate_terrain(self.dimensions[0], self.dimensions[1], terrain_type)

        self.water_level = 0.05

        self.placeWorms()

        self.top_left = (0, 0)

        self.current_player = None
        self.current_worm = None
        self.action_points = 0

        self.next_player_generator = self.getNextPlayer()

        self.next_turn()
        self.update()
        self.draw()

    def placeWorms(self):
        for player in self.players:
            for worm in player.worms:
                while True:
                    x = int(random() * (self.dimensions[0] - 1))
                    y = int(random() * (self.dimensions[1] - 1))
                    if self.terrain[x][y] == 0 and self.terrain[x][y + 1] == 1 and self.isUnderWater(y):
                        # if no worm is in a 5x5 square around the worm
                        if not any(
                                [any([w.x - 2 < x < w.x + 2 and w.y - 2 < y < w.y + 2 for w in player.worms]) for player
                                 in self.players]):
                            worm.x = x
                            worm.y = y
                            break

    def next_turn(self):
        self.current_player = next(self.next_player_generator)
        self.current_worm = next(self.current_player.next_worm_generator)
        # TODO: Balancer les points d'action (genre les déplacements, tout ça)
        self.action_points = 60
        print(f"Au tour de {self.current_player.color} avec le worm en: {self.current_worm.x}, {self.current_worm.y}")

    # Only applies explosion to the terrain
    # TODO: Apply explosion to worms + damage
    def applyExplosion(self, x, y, radius):
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i ** 2 + j ** 2 < radius ** 2:
                    if 0 < x + i < self.dimensions[0] and 0 < y + j < self.dimensions[1]:
                        self.terrain[x + i][y + j] = 0
                        self.game.window.set_at((x + i, y + j), (0, 0, 0))

    def getNextPlayer(self):
        while True:
            for player in self.players:
                print(player.color)
                if player.alive:
                    yield player

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = "main_menu"
        # TODO: Pour l'instant, enter --> prochain tour
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.next_turn()
            # TODO: Pour le reste des actions, utilisez current_worm

        # TODO: DEBUG: Pour tester l'explosion, appuyez sur la touche "e"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            print("Taille du terrain: ", self.dimensions)
            x = input("x: ")
            y = input("y: ")
            radius = input("radius: ")
            self.applyExplosion(int(x), int(y), int(radius))

        self.current_worm.events(event)

    def update(self):
        for entity in self.all_players_sprites:
            entity.update()
        self.draw()

    def isUnderWater(self, y):
        return y < self.dimensions[1] - (self.dimensions[1] * self.water_level)

    def draw(self):
        width = self.game.settings.width
        height = self.game.settings.height
        self.game.window.fill((255, 255, 255))

        # Draw the parts of the terrain that are visible TODO : DECOMMENTER ICI / MODIFIER UNE FOIS MODIF TERRAIN EFFECTUE, PARCE QUE LÀ ÇA LAGUE SA RACE

        # if self.top_left[0] < 0:
        #     self.top_left = (0, self.top_left[1])
        # if self.top_left[1] < 0:
        #     self.top_left = (self.top_left[0], 0)
        # if self.top_left[0] + width > self.dimensions[0]:
        #     self.top_left = (self.dimensions[0] - width, self.top_left[1])
        # if self.top_left[1] + height > self.dimensions[1]:
        #     self.top_left = (self.top_left[0], self.dimensions[1] - height)
        #
        # for x in range(width):
        #     for y in range(height):
        #         cell = self.terrain[x + self.top_left[0]][y + self.top_left[1]]
        #         if self.isUnderWater(y + self.top_left[1]):
        #             color = (255 * cell / 2, 255 * cell / 2, 255 * cell / 2)
        #         else:
        #             color = (0, 0, 255 * ((cell + 1) / 2))
        #
        #         self.game.window.set_at((x, y), color)

        pygame.draw.circle(self.game.window, (0, 0, 0), self.current_worm.pos, 20)

        for entity in self.all_sprites:
            self.game.window.blit(entity.surf, entity.rect)
