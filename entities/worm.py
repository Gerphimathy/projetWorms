from enum import Enum

import pygame

vec = pygame.math.Vector2

ACC = 0.5
FRIC = -0.12


class Direction(Enum):
    LEFT = -1
    NONE = 0
    RIGHT = 1


class Worm(pygame.sprite.Sprite): #TODO : ptetr faire une class Kinematic Sprite de laquelle hériterait les joueurs et les projectiles pour simplifier les formules de mouvement ?

    def __init__(self, x, y, player, sprites_groups, hp_p_worm=100):
        super().__init__()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

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

    def events(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jump()

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_RIGHT]:
                if pressed_keys[pygame.K_LEFT]:
                    self.direction = Direction.LEFT
                else:
                    self.direction = Direction.RIGHT
            else:
                self.direction = Direction.NONE
            self.acc.x = ACC * self.direction.value  # TODO: Je sais pas où placer ça, dans le move ou dans l'event ?

    def jump(self):
        print("jump")
        pass

    # TODO : JUMP

    def update(self): # TODO : Je sais pas si c'est ici mais ya un truc bizarre qui se passe, à fix
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
        print(self.pos, self.vel, self.acc) # TODO : REMOVE
