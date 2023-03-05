from enum import Enum

import pygame

import random
from typing import Generic, TypeVar

from entities.KinematicObject import KinematicObject
from entities.Grenade import Grenade
from entities.Rocket import Rocket
from entities.Teleport import Teleport

vec = pygame.math.Vector2

WIDTH = 5
HEIGHT = 15

VITESSE = 2.5
FORCE_DE_SAUT = 15

MIN_S_RADIUS = 30
MAX_S_RADIUS = 100

MIN_TIME = 2
MAX_TIME = 5

# Max force for grenade throw
MAX_FORCE = 50

W = TypeVar('W', bound=KinematicObject)


class Worm(KinematicObject):

    def __init__(self, x, y, player, sprites_groups, partie, hp_p_worm=100):
        super().__init__(x, y, partie.terrain, partie.terrain_sprite, partie,
                         wind_modifier=0, ground_fric_modifier=-0.7, fric_modifier=-0.1, grav_modifier=0.1)

        self.partie = partie
        self.player = player
        self.left = False
        self.right = False
        self.direction_modifier = 0
        self.length = 1
        self.body = (x, y)
        self.alive = True
        self.hp = hp_p_worm
        self.grounded = False
        self.canAttack = False

        self.surf = pygame.Surface((WIDTH, HEIGHT))
        self.surf.fill(self.player.color)
        self.rect = self.surf.get_rect()

        for g in sprites_groups:
            g.add(self)
        self.player.player_sprites.add(self)

        self.active = False
        self.dependants = []
        self.weapon = ""

        self.sound_goutte = pygame.mixer.Sound('assets/sounds/water_death.wav')
        self.sound_grenade_launcher = pygame.mixer.Sound('assets/sounds/grenade_launcher.wav')
        self.sound_cartoon_jump = pygame.mixer.Sound('assets/sounds/cartoon_jump.wav')
        self.sound_death = pygame.mixer.Sound('assets/sounds/death.wav')

    def events(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z or event.key == pygame.K_SPACE:
                    self.jump()
                if event.key == pygame.K_q:
                    self.left = True
                if event.key == pygame.K_d:
                    self.right = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.partie.game.state = "weapons_menu"
                if event.button == 1:
                    # if key exists in dict
                    if "weapon" in self.partie.game.states["weapons_menu"].data.keys() and self.partie.game.states["weapons_menu"].data["weapon"] != "":
                        self.weapon = self.partie.game.states["weapons_menu"].data["weapon"]
                        self.partie.game.states["weapons_menu"].data["weapon"] = ""
                        # Switch on weapon
                        if self.canAttack:
                            if "grenade" in self.weapon:
                                time = self.weapon.split(" ")[1]
                                time = int(time.split("s")[0])
                                parameters = {'time': time}
                                self.throw_weapon(Grenade, parameters=parameters)
                            if "rocket" in self.weapon:
                                self.throw_weapon(Rocket)
                            if "vest" in self.weapon:
                                self.s_vest()
                            if "teleport" in self.weapon:
                                self.throw_weapon(Teleport)
                            self.canAttack = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self.left = False
                if event.key == pygame.K_d:
                    self.right = False

            self.direction_modifier = -int(self.left) + int(self.right)

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
        force = self.partie.enterForceMode(MAX_FORCE)

        self.sound_grenade_launcher.play()

        if force > 30:
            force = 30
        if force < 0:
            force = 0

        if angle > 360:
            angle = 360
        if angle < 0:
            angle = 0

        self.dependants.append(W(self.x, self.y - HEIGHT, self.partie, self, angle, force, parameters))

    def s_vest(self):
        self.partie.applyExplosion(int(self.x), int(self.y), random.randint(MIN_S_RADIUS, MAX_S_RADIUS))
        pygame.event.clear()
        self.hp = 0

    def jump(self):
        if self.grounded:
            self.sound_cartoon_jump.play()
            self.addVelocityVector(
                vec(self.direction_modifier * FORCE_DE_SAUT, -FORCE_DE_SAUT).normalize() * FORCE_DE_SAUT
            )
            self.grounded = False

    def kill(self) -> None:
        self.sound_death.play()
        super().kill()
        self.alive = False
        self.player.player_sprites.remove(self)
        self.partie.all_sprites.remove(self)
        self.player.player_sprites.remove(self)
        self.player.worms.remove(self)
        for d in self.dependants:
            d.kill()
        if self.active:
            self.partie.next_turn()
            self.active = False

    def update(self):
        if self.active:
            if self.left or self.right:
                if self.grounded:
                    airborn_modifier = 1
                    if not self.collides():
                        self.y -= 1
                else:
                    airborn_modifier = 0.2
                self.addVelocityVector(vec(
                    self.direction_modifier * VITESSE * airborn_modifier, -VITESSE * 0.3 * airborn_modifier
                ))

        super().update()
        self.rect.midbottom = self.pos

        for d in self.dependants:
            d.update()

        if self.partie.isUnderWater(self.y):
            self.hp = 0
            self.sound_goutte.play()

        if self.hp <= 0:
            self.kill()

    def inRadius(self, x, y, radius):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= radius ** 2

    def processCollision(self, old_pos):
        super().processCollision(old_pos)
        self.grounded = True

    def processNoCollision(self):
        self.grounded = False
