import pygame

vec = pygame.math.Vector2


class Terrain(pygame.sprite.Sprite):
    def __init__(self, x, y, terrain_surface):
        super().__init__()
        self.pos = vec(x, y)
        self.surf = terrain_surface
        self.rect = self.surf.get_rect()

    def kill(self) -> None:
        super().kill()
        # Place a black pixel at self pos
        self.surf = None
        self.pos = None

    def in_radius(self, x, y, radius):
        return (self.pos.x - x) ** 2 + (self.pos.y - y) ** 2 <= radius ** 2

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
