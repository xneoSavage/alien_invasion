import pygame.font
import os


class Scoreboard:

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (214, 199, 199)
        self.font = pygame.font.SysFont(None, 26)
        self.records = './data/records.txt'
        self.prep_score()
        self.show_record()
        self.show_ships()
        self.show_level()

    def prep_score(self):
        self.rounded_score = round(self.stats.score, -1)
        self.score_str = "Score: {:,}".format(self.rounded_score)
        self.score_image = self.font.render(self.score_str, True,
                                            self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def show_record(self):
        with open(self.records, 'r') as f:
            if os.stat(self.records).st_size == 0:
                self.record = '0'
            else:
                self.record = int(f.readlines()[-1])
            f.close()

        self.last_record_image = self.font.render("Record: {:,}".format(self.record), True,
                                                  self.text_color)
        self.last_record_rect = self.last_record_image.get_rect()
        self.last_record_rect.top = 10
        self.last_record_rect.left = 20

    def show_interface(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.last_record_image, self.last_record_rect)
        self.screen.blit(self.ships_left_image, self.ships_left_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def write_records(self):
        with open(self.records, 'a') as f:
            if int(self.record) < self.rounded_score:
                f.write(f"\n{self.rounded_score}")
            f.close()

    def show_ships(self):
        self.ships_left_image = self.font.render("Left ships: {}".format(self.stats.ships_left), True,
                                                 self.text_color)
        self.ships_left_rect = self.ships_left_image.get_rect()
        self.ships_left_rect.top = 10
        self.ships_left_rect.right = 900

    def show_level(self):
        self.level_image = self.font.render("Level: {}".format(self.settings.level), True,
                                                 self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = 10
        self.level_rect.right = 1000