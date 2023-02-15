def pregame_menu_options():
    # Each name, function pair will be attributed to a menu_option object

    def player_count(self):
        def inner():
            self.menu.data['player_count'] = self.get_current_value()

        return inner

    def worms_per_player(self):
        def inner():
            self.menu.data['worms_per_player'] = self.get_current_value()

        return inner

    def map_type(self):
        def inner():
            self.menu.data['map_type'] = self.get_current_value()

        return inner

    def play(self):
        def inner():
            # Check for menu attributes and use defaults if not set
            if 'player_count' not in self.menu.data:
                self.menu.data['player_count'] = 2
            if 'worms_per_player' not in self.menu.data:
                self.menu.data['worms_per_player'] = 4
            if 'map_type' not in self.menu.data:
                self.menu.data['map_type'] = 'bumpy'

            self.menu.game.state = 'game'

        return inner

    def back(self):
        def inner():
            self.menu.game.state = "main_menu"

        return inner

    return [
        ('Lancer la partie', play, None),
        ('Nombre de joueurs', player_count, "lateral", [2, 3, 4], 2),
        ('Nombre de vers par joueur', worms_per_player, "lateral", [1, 2, 3, 4], 4),
        ('Type de carte', map_type, "lateral", ['bumpy', 'flat', 'mountainous', 'extreme', 'cave'], 'bumpy'),
        ('Retour', back, None)]
