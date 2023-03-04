import random

import pygame

from entities.KinematicObject import KinematicObject

vec = pygame.math.Vector2

MAX_RADIUS = 100
MIN_RADIUS = 30


class Rocket(KinematicObject):
    def __init__(self, x, y, partie, worm, angle, force, parameters: dict = {}):
        super().__init__(x, y, partie.terrain, partie.terrain_sprite, partie,
                         grav_modifier=0.03, wind_modifier=1, fric_modifier=-0.03)
        self.pos = vec(x, y)

        self.partie = partie
        self.worm = worm
        self.setVelocityAngle(angle, force)

        self.force = force
        self.angle = angle
        print(f"Rocket - Force: {self.force} Angle: {self.angle}")
        # Create a surface at x, y, fill it with a red circle and add it to all_sprites after blitting it

        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 0, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.partie.all_sprites.add(self)

    def update(self):
        super().update()
        # if self.vel == (0, 0):
        #     # Rebond
        #     self.force *= 0.5
        #     self.setVelocityAngle(self.angle, self.force)

        self.rect.midbottom = self.pos

    def processCollision(self, old_pos):
        self.kill()
        radius = random.randint(MIN_RADIUS, MAX_RADIUS)
        self.partie.applyExplosion(int(self.x), int(self.y), radius)
        self.worm.dependants.remove(self)
        self.partie.all_sprites.remove(self)
