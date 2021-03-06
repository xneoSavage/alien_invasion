import pygame.image


class Settings:
    """Клас для збереження налаштувань гри"""

    def __init__(self):
        """Ініціалізувати налаштування гри"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg = pygame.image.load('img/background.png')
        self.ship_speed = 1.5
        self.ship_limit = 3
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullet_allowed = 6

        self.alien_speed = 1.0
        self.fleet_drop_speed = 3
        self.fleet_direction = 1

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.init_dynamic_settings()
        self.level = 1

    def init_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.alien_speed = 1.0
        self.alien_points = 10
        self.fleet_direction = 1
        self.level = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        self.level += 1