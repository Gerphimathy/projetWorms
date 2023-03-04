from enum import Enum

import pygame

import random

from entities.KinematicObject import KinematicObject
from entities.Grenade import Grenade

vec = pygame.math.Vector2

VITESSE = 4
FORCE_DE_SAUT = 15

MIN_S_RADIUS = 30
MAX_S_RADIUS = 100

MIN_TIME = 2
MAX_TIME = 5

# Max force for grenade throw
MAX_FORCE = 50


class Direction(Enum):
    LEFT = -1
    NONE = 0
    RIGHT = 1


class Worm(KinematicObject):

    def __init__(self, x, y, player, sprites_groups, partie, hp_p_worm=100):
        super().__init__(x, y, partie.terrain, partie.terrain_sprite)

        self.partie = partie
        self.player = player
        self.direction = Direction.NONE
        self.length = 1
        self.body = (x, y)
        self.alive = True
        self.hp = hp_p_worm

        self.surf = pygame.Surface((5, 15))
        self.surf.fill(self.player.color)
        self.rect = self.surf.get_rect()

        for g in sprites_groups:
            g.add(self)
        self.player.player_sprites.add(self)

        self.active = False
        self.dependants = []

    def events(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jump()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_q] or pressed_keys[pygame.K_d]:
                if pressed_keys[pygame.K_q]:
                    self.direction = Direction.LEFT
                else:
                    self.direction = Direction.RIGHT
            else:
                self.direction = Direction.NONE
            if self.direction != Direction.NONE:
                self.addForce(self.x, self.y, 0, self.direction.value * VITESSE, self.player.game.settings.fps)

            if pressed_keys[pygame.K_g]:
                if not any(isinstance(d, Grenade) for d in self.dependants):
                    self.throw_grenade()
            if pressed_keys[pygame.K_s]:
                self.s_vest()

    def throw_grenade(self):
        target = self.partie.enterCrosshair()
        angle = self.partie.calculateAngle(self.pos, target)
        time = random.randint(MIN_TIME, MAX_TIME)
        force = self.partie.enterForceMode(MAX_FORCE)

        if force > 30:
            force = 30
        if force < 0:
            force = 0

        if angle > 360:
            angle = 360
        if angle < 0:
            angle = 0

        self.dependants.append(Grenade(self.x, self.y, self.partie, self, angle, force, time))

    def s_vest(self):
        self.partie.applyExplosion(int(self.x), int(self.y), random.randint(MIN_S_RADIUS, MAX_S_RADIUS))
        pygame.event.clear()
        self.active = False
        self.kill()
        self.partie.next_turn()

    def jump(self):
        self.addForce(self.x, self.y, 90, FORCE_DE_SAUT, self.player.game.settings.fps)

    def kill(self) -> None:
        super().kill()
        self.alive = False
        self.player.player_sprites.remove(self)
        self.partie.draw()

    def update(self):
        super().update()
        self.rect.midbottom = self.pos

        for d in self.dependants:
            d.update()

        if self.partie.isUnderWater(self.y):
            self.hp -= 1

        if self.hp <= 0:
            if self.active:
                self.partie.next_turn()
                self.active = False
            self.kill()

    def inRadius(self, x, y, radius):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= radius ** 2
