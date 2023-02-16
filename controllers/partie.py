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
        self.terrain = systems.terrain.generate_terrain(self.dimensions[0], self.dimensions[1], terrain_type)

        self.water_level = 0.05

        nb_worms = players * w_p_player
        parts = self.dimensions[0] // nb_worms
        ''' TODO 
        Place worms
        for k in range(nb_worms):
            player_index = k // w_p_player
            worm_index = k % w_p_player
            # If terrain type is flat, bumpy or mountain, place the worms at the top of the terrain
            if terrain_type in ["flat", "bumpy", "mountainous", "extreme"]:
                self.players[player_index].worms[worm_index].x = int(parts * (k + 0.5))
                for y in range(self.dimensions[1]):
                    if self.terrain[self.players[player_index].worms[worm_index].x][y] == 1:
                        self.players[player_index].worms[worm_index].y = y - 1
                        break

            # if terrain type is cave,
            # place the worms at a random x, with X y pair of coordinates,
            # within a horizontal slice of the terrain
            # within empty space and with ground below
            elif terrain_type == "cave":
                horizontal_slice = ((self.dimensions[0] // nb_worms) * k, (self.dimensions[0] // nb_worms) * (k + 1))
                # Divide the vertical space into three parts
                height_third = (k % 2) + 1
                vertical_slice = (self.dimensions[1] // (height_third + 1), self.dimensions[1] // height_third)
                for x in range(horizontal_slice[0], horizontal_slice[1]):
                    for y in range(vertical_slice[0], vertical_slice[1]):
                        if self.terrain[x][y] == 0 and self.terrain[x][y + 1] == 1:
                            self.players[player_index].worms[worm_index].x = x
                            self.players[player_index].worms[worm_index].y = y
                            break
        '''

        self.top_left = (0, 0)
        self.draw()

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
