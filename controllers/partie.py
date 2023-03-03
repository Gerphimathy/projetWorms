from random import random

import pygame

import entities.terrain
import systems.terrain

from entities.worm import Worm
from entities.player import Player

from entities.terrain import Terrain


class Partie:
    def __init__(self, game, players, w_p_player, terrain_type):
        if game is None:
            return

        self.game = game

        self.all_sprites = pygame.sprite.Group()
        self.all_players_sprites = pygame.sprite.Group()

        self.dimensions = (game.settings.width, game.settings.height)
        self.terrain_type = terrain_type
        self.worm_per_player = w_p_player

        self.water_level = 0.05

        # Generate sprite and surface based on terrain, ignore 0s in the array and only draw 1s
        self.terrain = systems.terrain.generate_terrain(self.dimensions[0], self.dimensions[1], terrain_type)
        self.terrain_sprite = pygame.sprite.Group()
        self.terrain_surface = pygame.Surface(self.dimensions)
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if self.terrain[x][y] == 1:
                    self.terrain_surface.set_at((x, y), (self.terrain[x][y] * 255 / 2, self.terrain[x][y] * 255 / 2, self.terrain[x][y] * 255 / 2))
                    self.terrain_sprite.add(entities.terrain.Terrain(x, y, self.terrain_surface))

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.players = [Player(colors[_], w_p_player, self.game, self, [self.all_sprites, self.all_players_sprites]) for _ in
                        range(players)]

        self.placeWorms()

        self.top_left = (0, 0)

        self.current_player = None
        self.current_worm = None
        self.action_points = 0

        self.next_player_generator = self.getNextPlayer()

        self.next_turn()
        self.draw()
        self.update()

    def placeWorms(self):
        for player in self.players:
            for worm in player.worms:
                while True:
                    x = int(random() * (self.dimensions[0] - 1))
                    y = int(random() * (self.dimensions[1] - 1))
                    if self.terrain[x][y] == 0 and self.terrain[x][y + 1] == 1 and not self.isUnderWater(y):
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
        for sprite in self.terrain_sprite:
            if sprite.inRadius(x, y, radius):
                # Remove sprite from surface
                self.terrain_surface.set_at((int(sprite.x), int(sprite.y)), (0, 0, 0))
                sprite.kill()
        for _x in range(x - radius//2, x + radius//2):
            for _y in range(y - radius//2, y + radius//2):
                self.terrain[_x][_y] = 0

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
        return not y < self.dimensions[1] - (self.dimensions[1] * self.water_level)

    '''
    def drawTerrainArea(self, _x, _y, width, height):
        # Draw terrain in specified area
        for x in range(_x, _x+width):
            for y in range(_y, _y+height):
                cell = self.terrain[x + self.top_left[0]][y + self.top_left[1]]
                if self.isUnderWater(y + self.top_left[1]):
                    color = (255 * cell / 2, 255 * cell / 2, 255 * cell / 2)
                else:
                    color = (0, 0, 255 * ((cell + 1) / 2))
                self.game.window.set_at((x, y), color)
    '''

    def draw(self):
        self.game.window.fill((0, 0, 0))

        self.game.window.blit(self.terrain_surface, (0, 0))

        # Draw water rectangle at the bottom of the screen
        pygame.draw.rect(self.game.window, (0, 0, 255), (0, self.dimensions[1] - (self.dimensions[1] * self.water_level), self.dimensions[0], self.dimensions[1] * self.water_level))

        for entity in self.all_sprites:
            self.game.window.blit(entity.surf, entity.rect)
