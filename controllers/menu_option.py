class MenuOption:
    def __init__(self, menu, text, action):
        self.text = text
        self.action = action(self)
        self.menu = menu
