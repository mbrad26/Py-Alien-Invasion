class Settings:

    def __init__(self):

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship, bullet and alien speeds settings.

        self.ships_limit = 3
        self.ships_allowed = 3
        self.bullets_allowed = 3
        self.alien_drop = 25
        self.alien_points = 50

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_settings()

    def initialize_settings(self):

        self.ship_speed = 1
        self.bullet_speed = 3
        self.alien_speed = .25
        self.change = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
