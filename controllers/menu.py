import pygame

from controllers.menu_option import MenuOption


class Menu:
    def __init__(self, name, game, options=None, style=None):
        self.texts = []
        self.name = name
        self.game = game
        options = options if options is not None else []
        self.options = [MenuOption(self, option[0], option[1]) for option in options]
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

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = self.__selected - 1
            elif event.key == pygame.K_DOWN:
                self.selected = self.__selected + 1
            elif event.key == pygame.K_RETURN:
                self.selected.action()

            self.update()

    def update(self):
        # For each text, if it is selected, draw it with the selected color, otherwise draw it with the normal color
        for i, text in enumerate(self.texts):
            if i == self.__selected:
                text = self.style['font'].render(self.options[i].text, True, self.style['font_selected_color'])
                self.texts[i] = text
                self.game.window.blit(text, (0, i * 30))
            else:
                text = self.style['font'].render(self.options[i].text, True, self.style['font_color'])
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
                        text = value.render(option.text, True, self.style['font_selected_color'])
                    else:
                        text = value.render(option.text, True, self.style['font_color'])
                    self.texts += (text,)
                    window.blit(text, (0, i * 30))

