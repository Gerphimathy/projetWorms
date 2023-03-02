import pygame

from controllers.menu_option import MenuOption, LateralMenuOption


class Menu:
    def __init__(self, name, game, options=None, style=None):
        self.data = {}
        self.texts = []
        self.name = name
        self.game = game
        self.options = options if options is not None else []
        for option in options:
            if option[2] is None:
                self.options[self.options.index(option)] = MenuOption(self, option[0], option[1])
            else:
                if option[2] == "lateral":
                    self.options[self.options.index(option)] = LateralMenuOption(self, option[0], option[1], option[3],
                                                                                 option[4])

        self.__selected = 0
        self.style = style if style is not None else {}

    def __get_selected(self):
        return self.options[self.__selected]

    def __set_selected(self, value):
        if value > len(self.options) - 1:
            value = 0
        elif value < 0:
            value = len(self.options) - 1
        self.__selected = value

    selected = property(__get_selected, __set_selected)

    def events(self, event):
        if self.game.state != self:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = self.__selected - 1
            elif event.key == pygame.K_DOWN:
                self.selected = self.__selected + 1
            elif event.key == pygame.K_RETURN:
                self.selected.action()
            elif event.key == pygame.K_LEFT:
                if self.selected.__class__.__name__ == 'LateralMenuOption':
                    self.selected.value = self.selected.value - 1
            elif event.key == pygame.K_RIGHT:
                if self.selected.__class__.__name__ == 'LateralMenuOption':
                    self.selected.value = self.selected.value + 1


    def update(self):
        if self.game.state != self:
            return
        # For each text, if it is selected, draw it with the selected color, otherwise draw it with the normal color

        for key, value in self.style.items():
            if key == 'background_color':
                self.game.window.fill(value)
            elif key == 'background_image' and value is not None:
                self.game.window.blit(value, (0, 0))

        for i, text in enumerate(self.texts):
            if i == self.__selected:
                text = self.style['font'].render(str(self.options[i]), True, self.style['font_selected_color'])
                self.texts[i] = text
                self.game.window.blit(text, (0, i * 30))
            else:
                text = self.style['font'].render(str(self.options[i]), True, self.style['font_color'])
                self.texts[i] = text
                self.game.window.blit(text, (0, i * 30))

    def draw(self, window):
        # Draw the menu using the style
        self.texts = []
        for key, value in self.style.items():
            if key == 'background_color':
                window.fill(value)
            elif key == 'background_image' and value is not None:
                window.blit(value, (0, 0))
            elif key == 'font':
                for i, option in enumerate(self.options):
                    if i == self.__selected:
                        text = value.render(str(option), True, self.style['font_selected_color'])
                    else:
                        text = value.render(str(option), True, self.style['font_color'])
                    self.texts += (text,)
                    window.blit(text, (0, i * 30))
