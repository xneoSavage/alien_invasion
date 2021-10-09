import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # Load the alien image and set rect attribute
        self.image = pygame.image.load('img/alien_ship1.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien at the top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        if self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0:
            return True

    def update(self):
        """Move left or right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
