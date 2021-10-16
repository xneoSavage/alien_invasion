class GameStats:
    """Game statistics"""

    def __init__(self, ai_game):
        """init statistic"""
        self.setting = ai_game.settings
        self.reset_stats()

        # Start game in inactive stste
        self.game_active = False

    def reset_stats(self):
        """Init stat what can change during game"""
        self.ships_left = self.setting.ship_limit



