from enum import Enum

import pygame

from entities.KinematicObject import KinematicObject

vec = pygame.math.Vector2

VITESSE = 4
FORCE_DE_SAUT = 15


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
        if self.partie.isUnderWater(self.y):
            self.hp -= 1

        if self.hp <= 0:
            if self.active:
                self.partie.next_turn()
                self.active = False
            self.kill()