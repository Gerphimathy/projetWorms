def weapons_options():
    def weapon(self):
        def inner():
            self.menu.data['weapon'] = self.get_current_value()
            self.menu.game.state = "game"

        return inner

    return [
        ('Arme', weapon, "lateral",
         ["grenade 2s", "grenade 3s", "grenade 4s", "grenade 5s", "vest", "rocket", "teleport"],
         "grenade 2s"),
    ]
