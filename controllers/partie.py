import math
import sys
from random import random

import pygame

import entities.terrain
import systems.terrain

import time

from entities.worm import Worm
from entities.player import Player

from entities.terrain import Terrain
from menu_actions.menu_style import default_menu_style

vec = pygame.math.Vector2


class Partie:
    def __init__(self, game, players, w_p_player, terrain_type):
        if game is None:
            return

        self.game = game

        self.GRAVITY = vec(0, 9)  # Positive gravity because the y-axis goes toward the ground

        self.all_sprites = pygame.sprite.Group()
        self.all_players_sprites = pygame.sprite.Group()

        self.dimensions = (game.settings.width, game.settings.height)
        self.terrain_type = terrain_type
        self.worm_per_player = w_p_player

        self.wind = vec(0, 0)
        self.wind_angle = 0
        self.__wind_arrow = False

        self.water_level = 0.05

        self.sound_explosion = pygame.mixer.Sound('assets/sounds/explosion.wav')

        # Generate sprite and surface based on terrain, ignore 0s in the array and only draw 1s
        self.terrain = systems.terrain.generate_terrain(self.dimensions[0], self.dimensions[1], terrain_type)
        self.terrain_sprite = pygame.sprite.Group()
        self.terrain_surface = pygame.Surface(self.dimensions)
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if self.terrain[x][y] == 1:
                    self.terrain_surface.set_at((x, y), (
                        self.terrain[x][y] * 255 / 2, self.terrain[x][y] * 255 / 2, self.terrain[x][y] * 255 / 2))
                    self.terrain_sprite.add(entities.terrain.Terrain(x, y, self.terrain_surface))

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        names = ["Rouge", "Vert", "Bleu", "Jaune", "Violet", "Cyan"]
        self.players = [
            Player(colors[_], names[_], w_p_player, self.game, self, [self.all_sprites, self.all_players_sprites])
            for _ in range(players)]

        self.n_b_players = players

        self.placeWorms()

        self.top_left = (0, 0)

        self.current_player = None
        self.current_worm = None
        self.action_points = 0

        self.next_player_generator = self.get_next_player()

        self.ranking = []

        self.__crosshair = False
        self.crosshair_target = (0, 0)

        self.__forceMode = False
        self.__max_force = 0
        self.__force_progress = 0

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
        if self.current_worm:
            self.current_worm.active = False
            (self.current_worm.left, self.current_worm.right) = (False, False)
            self.current_worm.direction_modifier = 0

        self.change_wind()
        self.current_player = next(self.next_player_generator)
        self.current_worm = next(self.current_player.next_worm_generator)
        self.current_worm.active = True
        self.current_worm.canAttack = True
        # TODO: Balancer les points d'action (genre les déplacements, tout ça)
        self.action_points = 60

    def applyExplosion(self, x, y, radius, damage=100):
        for sprite in self.terrain_sprite:
            if sprite.inRadius(x, y, radius):
                # Remove sprite from surface
                self.terrain_surface.set_at((int(sprite.x), int(sprite.y)), (0, 0, 0))
                sprite.kill()
            # (x - self.x) ** 2 + (y - self.y) ** 2 <= radius ** 2
        for _x in range(x - radius, x + radius):
            for _y in range(y - radius, y + radius):
                if _x < 0 or _x >= self.dimensions[0] or _y < 0 or _y >= self.dimensions[1]:
                    continue
                if (x - _x) ** 2 + (y - _y) ** 2 <= radius ** 2:
                    self.terrain[_x][_y] = 0

        for player in self.players:
            for worm in player.worms:
                if worm.inRadius(x, y, radius):
                    epi_to_worm_vec = (worm.x - x, worm.y - y)
                    distance = math.sqrt(epi_to_worm_vec[0] ** 2 + epi_to_worm_vec[1] ** 2)
                    worm.hp -= damage * (1 - distance / radius)
                    worm.setVelocityAngle(
                        self.calculateAngle((x, y), worm.pos),
                        20 * (1 - distance / radius)
                    )

        self.sound_explosion.play()

    def enterCrosshair(self):
        pygame.event.clear()
        self.__crosshair = True
        selected = False
        while not selected:
            pygame.event.pump()
            self.crosshair_target = pygame.mouse.get_pos()
            self.draw()
            pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                selected = True
        self.__crosshair = False
        self.draw()
        return self.crosshair_target

    def enterForceMode(self, max_power):
        pygame.event.clear()
        self.__forceMode = True
        self.__max_force = max_power
        self.__force_progress = 0

        direction = 1 / (self.game.settings.fps / 3)

        self.draw()
        pygame.display.update()

        time.sleep(1)

        while not pygame.mouse.get_pressed()[0]:
            pygame.event.pump()
            self.draw()
            pygame.display.update()
        while self.__forceMode:
            pygame.event.pump()
            self.draw()
            pygame.display.update()
            self.__force_progress += direction
            if self.__force_progress >= max_power or self.__force_progress <= 0:
                direction *= -1
            if not pygame.mouse.get_pressed()[0]:
                self.__forceMode = False
        self.draw()
        return self.__force_progress

    def calculateAngle(self, origin, target):
        base_vec = (1, 0)
        target_vec = (target[0] - origin[0], target[1] - origin[1])
        try:
            angle = math.acos((base_vec[0] * target_vec[0] + base_vec[1] * target_vec[1]) / (
                    math.sqrt(base_vec[0] ** 2 + base_vec[1] ** 2) * math.sqrt(
                target_vec[0] ** 2 + target_vec[1] ** 2)))
        except ZeroDivisionError:
            angle = math.pi / 2

        if target[1] > origin[1]:
            angle = math.pi * 2 - angle
        return math.degrees(angle)

    def get_next_player(self):
        while True:
            for player in self.players:
                if player.alive:
                    yield player

    def change_wind(self):
        self.__wind_arrow = True
        self.wind = vec(random() * 2 - 1, random() * 2 - 1).normalize() * random() * 10
        self.wind_angle = self.calculateAngle((0, 0), self.wind)
        self.draw()
        self.__wind_arrow = False

    def rotate_point(self, point, pivot, angle):
        x, y = point
        px, py = pivot
        angle = math.radians(angle)
        qx = px + math.cos(angle) * (x - px) - math.sin(angle) * (y - py)
        qy = py + math.sin(angle) * (x - px) + math.cos(angle) * (y - py)
        return int(qx), int(qy)

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = "main_menu"
        # TODO: Afficher les touches pour les actions
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.next_turn()
        self.current_worm.events(event)

    def update(self):
        if len(self.players) < 2:
            self.end_game()
        for player in self.players:
            player.update()
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

    def draw(self, window=None):
        self.game.window.fill((0, 0, 0))

        self.game.window.blit(self.terrain_surface, (0, 0))

        # Draw water rectangle at the bottom of the screen
        pygame.draw.rect(self.game.window, (0, 0, 255),
                         (0, self.dimensions[1] - (self.dimensions[1] * self.water_level), self.dimensions[0],
                          self.dimensions[1] * self.water_level))

        for entity in self.all_sprites:
            self.game.window.blit(entity.surf, entity.rect)

        for player in self.players:
            for worm in player.worms:
                if worm.active:
                    pygame.draw.circle(self.game.window, (255, 255, 255), (worm.x, worm.y), 10, 1)
                    break

        if self.__crosshair:
            pygame.draw.circle(self.game.window, (255, 0, 0), self.crosshair_target, 10, 1)
        if self.__forceMode:
            # Draw a circle in the center of the screen of dimensions height//10
            pygame.draw.circle(self.game.window, (255, 0, 0), (self.dimensions[0] // 2, self.dimensions[1] // 2),
                               self.dimensions[1] // 10, 1)
            # Draw a circle in the center of the screen, with a radius dependant on the force and with max radius of
            # height//10 when force is max
            pygame.draw.circle(self.game.window, (255, 0, 0), (self.dimensions[0] // 2, self.dimensions[1] // 2),
                               int(self.__force_progress * self.dimensions[1] / 10 / self.__max_force), 1)
        if self.__wind_arrow:
            arrow_position = (self.game.settings.width - 100, 50)
            arrow_points = [(0, 0), (0, -50), (200, 0), (0, 50)]
            rotated_points = []
            for point in arrow_points:
                rotated_point = self.rotate_point(point, (0, 0), self.wind_angle)
                rotated_points.append((rotated_point[0] + arrow_position[0], rotated_point[1] + arrow_position[1]))
            pygame.draw.polygon(self.game.window, (255, 0, 0), rotated_points)

            # TODO: polygon test to remove later
            pygame.draw.polygon(self.game.window, (255, 0, 0), [(50, 50), (200, 70), (400, 60), (120, 120)])

    def end_game(self):
        if len(self.players) >= 1:
            self.ranking.append(self.players[0].name)

        style = default_menu_style()
        for key, value in style.items():
            if key == 'background_color':
                self.game.window.fill(value)
            elif key == 'background_image' and value is not None:
                self.game.window.blit(value, (0, 0))
            elif key == 'font':
                for player_name in self.ranking:
                    rank = self.n_b_players - self.ranking.index(player_name)
                    text = value.render(f"{rank} : {player_name}", True, style['font_color'])
                    self.game.window.blit(text, (0, rank * 30))

        in_loop = True
        while in_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    in_loop = False
            pygame.display.update()
        self.game.state = "main_menu"
