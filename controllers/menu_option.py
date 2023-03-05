class MenuOption:
    def __init__(self, menu, text, action):
        self.text = text
        self.action = action(self)
        self.menu = menu

    def __str__(self):
        return self.text


class LateralMenuOption(MenuOption):
    def __init__(self, menu, text, action, possible_values, default_value):
        super().__init__(menu, text, action)
        self.possible_values = possible_values
        self.__current_value = default_value
        self.__value = self.possible_values.index(self.__current_value)

    def __str__(self):
        return f"< {self.text} : {str(self.__current_value)} >"

    def get_current_value(self):
        return self.__current_value

    def __get_value(self):
        return self.__value

    def __set_value(self, value):
        if value > len(self.possible_values) - 1:
            value = 0
        elif value < 0:
            value = len(self.possible_values) - 1
        self.__value = value
        self.__current_value = self.possible_values[self.__value]

    value = property(__get_value, __set_value)
