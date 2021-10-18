import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Загальний клас який керує ресурсами та поведінкою гри"""

    def __init__(self):
        """Ініціалізація гри, створення ресурсів гри"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # create stats when game start
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        pygame.display.set_caption('Alien Invasion')
        self.bg = pygame.image.load('img/background.png')
        self.ship = Ship(self)
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.play_button = Button(self, 'Play')
        self.pause_button = Button(self, 'Pause')

        self.shot_sound = pygame.mixer.Sound('sound/spaceship_shot.wav')

    def run_game(self):
        """Розпочати головний цикл гри"""
        self._create_fleet()
        while True:
            self._check_events()
            self._check_bullet_alien_collisions()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Реагувати на натискання клавіартури та миші"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self._pause_game()
        elif event.key == pygame.K_l:
            self.settings.increase_speed()
        elif event.key == pygame.K_SPACE:
            if not self.stats.game_active and pygame.mouse.get_visible():
                self._start_game()
            else:
                self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed and self.stats.game_active:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.shot_sound.play()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


    def _create_fleet(self):
        # Create aliens fleet
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Create first row of aliens
        print(f'Number rows is {number_rows}\nNumber aliens {number_aliens_x}')
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number, alien_width, alien_height)

    def _create_alien(self, alien_number, row_number, alien_width, alien_height):
        # Create alien and set them to row
        alien = Alien(self)
        alien.x = alien_width + alien_number * alien_width * 2
        alien.y = alien_height + row_number * alien_height * 2
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        print(self.aliens)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_directions()
                break

    def _change_fleet_directions(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            print(collisions)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # if spaceship hits with alien
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_alien_bottom()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self._update_screen()
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            print(self.stats.ships_left)
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.settings.init_dynamic_settings()
            pygame.mouse.set_visible(True)
            self.sb.write_records()

    def _check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.stats.game_active != True:
            pygame.mouse.set_visible(False)
            self.sb.prep_score()
            self._start_game()

    def _start_game(self):
        self.sb.show_record()
        pygame.mouse.set_visible(False)
        self.stats.reset_stats()
        self.stats.game_active = True

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()

    def _pause_game(self):
        if self.stats.game_active:
            self.stats.game_active = False
        else:
            self.stats.game_active = True

    def _update_screen(self):
        """Оновлювати зображення на екрані та перемканутися на новий екран"""
        self.screen.blit(self.settings.bg.convert(), (0, 0))
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active and pygame.mouse.get_visible():
            self.play_button.draw_button()
        elif not self.stats.game_active:
            self.pause_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    """Створити екземпляр гри та запустити гру"""
    ai = AlienInvasion()
    ai.run_game()
