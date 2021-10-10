import pygame


class Ship:

    def __init__(self, ai_game):
        """Ініціалізація корабля, формування його вихідної позиції"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        """Завантажити зображення корабля, отримати його rect"""
        self.image = pygame.image.load('img/spaceship1.bmp')
        self.rect = self.image.get_rect()

        """Створювати кожен новий корабель внизу екрану, по центру"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        if self.moving_up or self.moving_down:
            self.rect.y = self.y
        if self.moving_left or self.moving_right:
            self.rect.x = self.x

    def blitme(self):
        """Намалювати корабель у поточному розташуванні"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = self.rect.x
        self.y = self.rect.y
