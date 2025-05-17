import json
from pathlib import Path

class GameStats:
    #Tracks statistics for Alien Invasion.
    
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        # High score should never be reset.
        self.high_score = self.get_saved_high_score()
        
    def get_saved_high_score(self):
        """Gets high score from file, if it exists."""
        path = Path('high_score.json')
        try:
            contents = path.read_text()
            high_score = json.loads(contents)
            return high_score
        except FileNotFoundError:
            return 0
        
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        