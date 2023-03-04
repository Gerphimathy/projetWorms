from enum import Enum

import pygame

import random
from typing import Generic, TypeVar

from entities.KinematicObject import KinematicObject
from entities.Grenade import Grenade
from entities.Rocket import Rocket

vec = pygame.math.Vector2

WIDTH = 5
HEIGHT = 15

VITESSE = 4
FORCE_DE_SAUT = 15

MIN_S_RADIUS = 30
MAX_S_RADIUS = 100

MIN_TIME = 2
MAX_TIME = 5

# Max force for grenade throw
MAX_FORCE = 50

W = TypeVar('W', bound=KinematicObject)


class Direction(Enum):
    LEFT = -1
    NONE = 0
    RIGHT = 1


class Worm(KinematicObject):

    def __init__(self, x, y, player, sprites_groups, partie, hp_p_worm=100):
        super().__init__(x, y, partie.terrain, partie.terrain_sprite, partie, wind_modifier=0)

        self.partie = partie
        self.player = player
        self.direction = Direction.NONE
        self.length = 1
        self.body = (x, y)
        self.alive = True
        self.hp = hp_p_worm
        self.grounded = False

        self.surf = pygame.Surface((WIDTH, HEIGHT))
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
                if event.key == pygame.K_g:
                    if not any(isinstance(d, Grenade) for d in self.dependants):
                        parameters = {'time' : random.randint(MIN_TIME, MAX_TIME)}
                        self.throw_weapon(Grenade, parameters=parameters)
                if event.key == pygame.K_s:
                    self.s_vest()
                if event.key == pygame.K_r:
                    if not any(isinstance(d, Rocket) for d in self.dependants):
                        self.throw_weapon(Rocket)

            pressed_keys = pygame.key.get_pressed()

            if self.grounded:
                if pressed_keys[pygame.K_q] or pressed_keys[pygame.K_d]:
                    if pressed_keys[pygame.K_q]:
                        self.direction = Direction.LEFT
                    else:
                        self.direction = Direction.RIGHT
                else:
                    self.direction = Direction.NONE
                if self.direction != Direction.NONE:
                    self.addVelocityVector(vec(self.direction.value * VITESSE, 0))

        # def throw_grenade(self):
        #     target = self.partie.enterCrosshair()
        #     angle = self.partie.calculateAngle(self.pos, target)
        #     time = random.randint(MIN_TIME, MAX_TIME)
        #     force = self.partie.enterForceMode(MAX_FORCE)
        #
        #     if force > 30:
        #         force = 30
        #     if force < 0:
        #         force = 0
        #
        #     if angle > 360:
        #         angle = 360
        #     if angle < 0:
        #         angle = 0
        #
        #     self.dependants.append(Grenade(self.x, self.y, self.partie, self, angle, force, time))
        #
        #     def throw_rocket(self):
        #         target = self.partie.enterCrosshair()
        #         angle = self.partie.calculateAngle(self.pos, target)
        #         time = random.randint(MIN_TIME, MAX_TIME)
        #         force = self.partie.enterForceMode(MAX_FORCE)
        #
        #         if force > 30:
        #             force = 30
        #         if force < 0:
        #             force = 0
        #
        #         if angle > 360:
        #             angle = 360
        #         if angle < 0:
        #             angle = 0
        #
        #         self.dependants.append(Rocket(self.x, self.y, self.partie, self, angle, force, time))

    def throw_weapon(self, W, parameters: list = []):
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

        self.dependants.append(W(self.x, self.y-HEIGHT, self.partie, self, angle, force, parameters))

    def s_vest(self):
        self.partie.applyExplosion(int(self.x), int(self.y), random.randint(MIN_S_RADIUS, MAX_S_RADIUS))
        pygame.event.clear()
        self.hp = 0

    def jump(self):
        if self.grounded:
            self.addVelocityAngle(90, FORCE_DE_SAUT)
            self.grounded = False

    def kill(self) -> None:
        super().kill()
        self.alive = False
        self.player.player_sprites.remove(self)
        self.partie.all_sprites.remove(self)
        self.player.player_sprites.remove(self)
        if self.active:
            self.partie.next_turn()
            self.active = False

    def update(self):
        super().update()
        self.rect.midbottom = self.pos

        for d in self.dependants:
            d.update()

        if self.partie.isUnderWater(self.y):
            self.hp = 0

        if self.hp <= 0:
            self.kill()

    def inRadius(self, x, y, radius):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= radius ** 2

    def processCollision(self, old_pos):
        super().processCollision(old_pos)
        self.grounded = True
