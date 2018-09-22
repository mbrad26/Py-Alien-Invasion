class Stats:
    def __init__(self, settings):
        self.settings = settings
        self.ships_limit = settings.ships_allowed
        self.game_active = True

