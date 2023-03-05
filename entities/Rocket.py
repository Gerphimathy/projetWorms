import random

import pygame

from entities.KinematicObject import KinematicObject

vec = pygame.math.Vector2

MAX_RADIUS = 100
MIN_RADIUS = 30


class Rocket(KinematicObject):
    def __init__(self, x, y, partie, worm, angle, force, parameters: dict = {}):
        super().__init__(x, y, partie.terrain, partie.terrain_sprite, partie,
                         grav_modifier=0.03, wind_modifier=0.03, fric_modifier=-0.03)
        self.pos = vec(x, y)

        self.partie = partie
        self.worm = worm
        self.set_velocity_angle(angle, force)

        self.force = force
        self.angle = angle

        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 0, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.partie.all_sprites.add(self)

    def update(self):
        super().update()
        self.rect.midbottom = self.pos

    def process_collision(self, old_pos):
        self.kill()
        radius = random.randint(MIN_RADIUS, MAX_RADIUS)
        self.partie.apply_explosion(int(self.x), int(self.y), radius)
        self.worm.dependants.remove(self)
        self.partie.all_sprites.remove(self)
        self.partie.next_turn()
