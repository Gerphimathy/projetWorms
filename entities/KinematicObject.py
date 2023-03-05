import math

import pygame

vec = pygame.math.Vector2


class KinematicObject(pygame.sprite.Sprite):
    def __init__(self, x, y, terrain, terrain_sprite_group, partie,
                 grav_modifier=0.1, wind_modifier=0.1, fric_modifier=-0.06, ground_fric_modifier=-0.3,
                 bounce_modifier=0.3):
        super().__init__()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.terrain = terrain
        self.terrain_sprite_group = terrain_sprite_group
        self.partie = partie
        self.grav_modifier = grav_modifier  # Can be understood as weight of the object
        self.wind_modifier = wind_modifier
        self.fric_modifier = fric_modifier
        self.ground_fric_modifier = ground_fric_modifier
        self.bounce_modifier = bounce_modifier

    def _get_x(self):
        return self.pos.x

    def _get_y(self):
        return self.pos.y

    def _set_x(self, x):
        self.pos = vec(x, self._get_y())

    def _set_y(self, y):
        self.pos = vec(self._get_x(), y)

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)

    def set_velocity_angle(self, angle, force):
        angle = math.radians(angle)

        self.vel = vec(
            force * math.cos(angle),
            -force * math.sin(angle)
        )

    def set_velocity_vector(self, vector: vec):
        self.vel = vector

    def add_velocity_angle(self, angle, force):
        angle = math.radians(angle)

        self.vel += vec(
            force * math.cos(angle),
            -force * math.sin(angle)
        )

    def add_velocity_vector(self, vector: vec):
        self.vel += vector

    def get_collision_surface(self):
        x = int(self.x)
        y = int(self.y)
        # produce a vector of the surface of the terrain the object is colliding with

        # get adjacent tiles
        adjacent = {}
        for _x in range(-4, 4):
            for _y in range(-4, 4):
                if not \
                        (x + _x < 0 or x + _x >= self.partie.dimensions[0] or
                         y + _y < 0 or y + _y >= self.partie.dimensions[1]):
                    adjacent[(x + _x, y + _y)] = self.terrain[x + _x][y + _y]

        # remove 0 values
        for values in adjacent.copy():
            if adjacent[values] == 0:
                del adjacent[values]

        adjacent = list(adjacent.keys())

        # Remove non surface tiles (have 4 adjacent tiles)
        for tile in adjacent.copy():
            # Ig at the limit of the map remove
            if tile[0] == 0 or tile[0] == self.partie.dimensions[0] - 1 or \
                    tile[1] == 0 or tile[1] == self.partie.dimensions[1] - 1:
                adjacent.remove(tile)
                continue
            if self.terrain[tile[0] + 1][tile[1]] != 0 and \
                    self.terrain[tile[0] - 1][tile[1]] != 0 and \
                    self.terrain[tile[0]][tile[1] + 1] != 0 and \
                    self.terrain[tile[0]][tile[1] - 1] != 0:
                adjacent.remove(tile)

        # Draw a vector from the first tile to the last
        if len(adjacent) > 1:
            return vec(vec(adjacent[-1]) - vec(adjacent[0]))
        else:
            return vec(0, 0)

    def collides(self):
        condition = (self.terrain[int(self.pos.x)][int(self.pos.y)] == 1 or
                     self.pos.x < 1 or self.pos.y >= self.partie.dimensions[0] - 1 or
                     self.pos.x < 1 or self.pos.y >= self.partie.dimensions[1] - 1
                     )
        return condition

    def update(self):
        old_pos = self.pos

        self.vel += self.partie.GRAVITY * self.grav_modifier
        self.vel += self.partie.wind * self.wind_modifier
        self.vel += self.vel * self.fric_modifier

        self.x += self.vel.x
        self.y += self.vel.y

        height = len(self.terrain[0]) - 1
        width = len(self.terrain) - 1

        if int(self.x) < 0 or int(self.x) > width:
            if int(self.x) < 0:
                self.x = 0
            elif int(self.x) > width:
                self.x = width

        if int(self.y) < 0 or int(self.y) > height:
            if int(self.y) < 0:
                self.y = 0
            elif int(self.y) > height:
                self.y = height

        if self.collides():
            self.process_collision(old_pos)
        else:
            self.process_no_collision()

    def process_collision(self, old_pos):
        normal = self.get_collision_surface().rotate(90)
        self.pos = old_pos
        self.add_velocity_vector(self.vel * self.ground_fric_modifier)
        self.bounce(normal)

    def bounce(self, normal: vec = vec(0, -1)):
        if normal.length() > 0 and self.vel != vec(0, 0):
            self.add_velocity_vector((self.vel.reflect(normal) - self.vel).normalize() * self.vel.length())
        else:
            self.set_velocity_vector(-self.vel)

    def process_no_collision(self):
        pass
