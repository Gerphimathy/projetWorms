import pygame

import systems.terrain


class Partie:
    def __init__(self, players, w_p_player, game):
        if game is None:
            return

        self.players = players
        self.game = game
        self.w_p_player = w_p_player
        self.turn = 0
        # Todo: Terrain size parameters and handle screen size being bigger than terrain size
        self.dimensions = (2000, 2000)
        terrain_type = input("Terrain type (flat, cave, bumpy, mountainous): ")
        self.terrain = systems.terrain.generate_terrain(self.dimensions[0], self.dimensions[1], terrain_type)
        print("Terrain generated")
        self.top_left = (0, 0)
        self.draw()

    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.state = "pause_menu"

        keys = pygame.key.get_pressed()
        # Get 5 % of the dimensions of the window
        if keys[pygame.K_LEFT]:
            self.top_left = (self.top_left[0] - self.game.settings.width // 20, self.top_left[1])
            self.draw()
        if keys[pygame.K_RIGHT]:
            self.top_left = (self.top_left[0] + self.game.settings.width // 20, self.top_left[1])
            self.draw()
        if keys[pygame.K_UP]:
            self.top_left = (self.top_left[0], self.top_left[1] - self.game.settings.height // 20)
            self.draw()
        if keys[pygame.K_DOWN]:
            self.top_left = (self.top_left[0], self.top_left[1] + self.game.settings.height // 20)
            self.draw()

    def update(self):
        pass

    def draw(self):
        width = self.game.settings.width
        height = self.game.settings.height
        self.game.window.fill((255, 255, 255))

        # Draw the parts of the terrain that are visible

        if self.top_left[0] < 0:
            self.top_left = (0, self.top_left[1])
        if self.top_left[1] < 0:
            self.top_left = (self.top_left[0], 0)
        if self.top_left[0] + width > self.dimensions[0]:
            self.top_left = (self.dimensions[0] - width, self.top_left[1])
        if self.top_left[1] + height > self.dimensions[1]:
            self.top_left = (self.top_left[0], self.dimensions[1] - height)

        for x in range(width):
            for y in range(height):
                cell = self.terrain[x + self.top_left[0]][y + self.top_left[1]]
                color = (255 * cell / 2, 255 * cell / 2, 255 * cell / 2)
                self.game.window.set_at((x, y), color)
