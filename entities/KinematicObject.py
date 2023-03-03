import math

import pygame

vec = pygame.math.Vector2

ACC = 0.5
FRIC = 0.12
GRAV = -9


class KinematicObject(pygame.sprite.Sprite):
    def __init__(self, x, y, terrain, terrain_sprite_group):
        super().__init__()
        self.pos = vec(x, y)
        self.terrain = terrain
        self.terrain_sprite_group = terrain_sprite_group
        self.forces = []

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

    def addForce(self, x0, y0, angle, force, refresh_rate):
        angle = math.radians(angle)

        def inner():
            t = 0.0
            # angle is provided in degrees, but we need radians
            while True:
                # TODO: Calculs avec frottements
                yield vec(
                    # V0*cos(a)
                    force * math.cos(angle),

                    # Grav*t²/2 + V0*sin(a)*t
                    # Inverted because pygame's y-axis is inverted
                    -force * math.sin(angle) - (GRAV * t)
                )
                t += 1 / (refresh_rate // 10)

        self.forces.append(inner())

    def collidesWith(self, all_terrain_sprites):
        # all_terrain_sprites is a pygame.sprite.Group
        return pygame.sprite.spritecollide(self, all_terrain_sprites, False)

    def update(self):
        old_pos = self.pos
        for force in self.forces:
            velocity = next(force)
            self.x += velocity.x
            self.y += velocity.y

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
                    self.forces = []
                    break

        if self.terrain[int(self.x)][int(self.y)] == 1:
            self.x = old_pos.x
            self.forces = []

