import math

import pygame

vec = pygame.math.Vector2


class KinematicObject(pygame.sprite.Sprite):
    def __init__(self, x, y, terrain, terrain_sprite_group, partie,
                 grav_modifier=0.1, wind_modifier=0.1, fric_modifier=-0.06):
        super().__init__()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.terrain = terrain
        self.terrain_sprite_group = terrain_sprite_group
        self.partie = partie
        self.grav_modifier = grav_modifier  # Can be understood as weight of the object
        self.wind_modifier = wind_modifier
        self.fric_modifier = fric_modifier

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

    def setVelocityAngle(self, angle, force):
        angle = math.radians(angle)

        self.vel = vec(
            force * math.cos(angle),
            -force * math.sin(angle)
        )

    def setVelocityVector(self, vector: vec):
        self.vel = vector

    def addVelocityAngle(self, angle, force):
        angle = math.radians(angle)

        self.vel += vec(
            force * math.cos(angle),
            -force * math.sin(angle)
        )

    def addVelocityVector(self, vector: vec):
        self.vel += vector

    def getCollisionSurface(self):
        x = int(self.x)
        y = int(self.y)
        # produce a vector of the surface of the terrain the object is colliding with

        # get adjacent tiles
        adjacents = {}
        for _x in range(-4, 4):
            for _y in range(-4, 4):
                if x + _x < 0 or x + _x >= self.partie.dimensions[0] or y + _y < 0 or y + _y >= self.partie.dimensions[1]:
                    continue
                adjacents[(x + _x, y + _y)] = self.terrain[x + _x][y + _y]

        # remove 0 values
        for values in adjacents.copy():
            if adjacents[values] == 0:
                del adjacents[values]

        adjacents = list(adjacents.keys())

        # Remove non surface tiles (have 4 adjacent tiles)
        for tile in adjacents.copy():
            if self.terrain[tile[0] + 1][tile[1]] != 0 and \
                    self.terrain[tile[0] - 1][tile[1]] != 0 and \
                    self.terrain[tile[0]][tile[1] + 1] != 0 and \
                    self.terrain[tile[0]][tile[1] - 1] != 0:
                adjacents.remove(tile)

        # Draw a vector from the first tile to the last
        if len(adjacents) > 1:
            return vec(vec(adjacents[-1]) - vec(adjacents[0]))
        else:
            return vec(0, 0)

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

        # if colliding bellow with terrain, undo y movement and place on ground level
        if self.terrain[int(self.x)][int(self.y)] == 1:
            for y in range(int(old_pos.y), int(self.pos.y)):
                if self.terrain[int(self.x)][y] == 1:
                    self.pos = vec(self.x, y - 1)
                    self.vel = vec(0, 0)
                    break

        if self.terrain[int(self.x)][int(self.y)] == 1:
            self.x = old_pos.x
            self.vel = vec(0, 0)
