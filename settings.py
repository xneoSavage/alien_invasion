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

        self.bullet_speed = 1.3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullet_allowed = 6

        self.alien_speed = .5
        self.fleet_drop_speed = 3
        self.fleet_direction = 1

