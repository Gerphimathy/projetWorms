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

        # TODO: color choice ?
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.players = [Player(colors[_], w_p_player, self.game) for _ in range(players)]

        # Todo: Terrain size parameters and handle screen size being bigger than terrain size
        self.dimensions = (game.settings.width, game.settings.height)
        self.terrain_type = terrain_type
        self.worm_per_player = w_p_player
        self.terrain = systems.terrain.generate_terrain(self.dimensions[0], self.dimensions[1], terrain_type)

        self.water_level = 0.05

        self.placeWorms()

        self.top_left = (0, 0)
        self.draw()

    def placeWorms(self):
        for player in self.players:
            for worm in player.worms:
                while True:
                    x = int(random() * (self.dimensions[0]-1))
                    y = int(random() * (self.dimensions[1]-1))
                    if self.terrain[x][y] == 0 and self.terrain[x][y+1] == 1 and self.isUnderWater(y):
                        # if no worm is in a 5x5 square around the worm
                        if not any([any([w.x - 2 < x < w.x + 2 and w.y - 2 < y < w.y + 2 for w in player.worms]) for player in self.players]):
                            worm.x = x
                            worm.y = y
                            break


    def getNextPlayer(self):
        while True:
            for player in self.players:
                if player.alive:
                    yield player

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = "main_menu"

    def update(self):
        pass

    def isUnderWater(self, y):
        return y < self.dimensions[1] - (self.dimensions[1] * self.water_level)

    def draw(self):
        width = self.game.settings.width
        height = self.game.settings.height
        self.game.window.fill((255, 255, 255))

        # Draw the parts of the terrain that are visible

        if self.top_left[0] < 0:
            self.top_left = (0, self.top_left[1])
        if self.top_left[1] < 0:
            self.top_left = (self.top_left[0], 0)
        if self.top_left[0] + width > self.dimensions[0]:
            self.top_left = (self.dimensions[0] - width, self.top_left[1])
        if self.top_left[1] + height > self.dimensions[1]:
            self.top_left = (self.top_left[0], self.dimensions[1] - height)

        for x in range(width):
            for y in range(height):
                cell = self.terrain[x + self.top_left[0]][y + self.top_left[1]]
                if self.isUnderWater(y + self.top_left[1]):
                    color = (255 * cell / 2, 255 * cell / 2, 255 * cell / 2)
                else:
                    color = (0, 0, 255 * ((cell+1)/2))

                self.game.window.set_at((x, y), color)

        for player in self.players:
            for worm in player.worms:
                if not worm.alive:
                    continue
                if worm.x < self.top_left[0] or worm.x > self.top_left[0] + self.game.settings.width:
                    continue
                if worm.y < self.top_left[1] or worm.y > self.top_left[1] + self.game.settings.height:
                    continue
                worm.draw()
