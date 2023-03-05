import random

import pygame

from entities.KinematicObject import KinematicObject

vec = pygame.math.Vector2

MAX_RADIUS = 100
MIN_RADIUS = 30


class Grenade(KinematicObject):
    def __init__(self, x, y, partie, worm, angle, force, parameters=None):
        super().__init__(x, y, partie.terrain, partie.terrain_sprite, partie, wind_modifier=0, fric_modifier=-0.02)
        if parameters is None:
            parameters = {}
        self.pos = vec(x, y)

        self.partie = partie
        self.worm = worm
        self.set_velocity_angle(angle, force)

        self.force = force
        self.angle = angle
        self.time = parameters['time'] * self.partie.game.settings.fps
        # Create a surface at x, y, fill it with a red circle and add it to all_sprites after blitting it

        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 0, 0))
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

        self.time -= 1

        if self.time <= 0:
            self.kill()
            radius = random.randint(MIN_RADIUS, MAX_RADIUS)
            self.partie.apply_explosion(int(self.x), int(self.y), radius)
            self.worm.dependants.remove(self)
            self.partie.all_sprites.remove(self)
            self.partie.next_turn()
