class Settings:
    
    def __init__(self):
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        #Ship Settings
        self.ship_limit = 3
        
        #Bullets
        self.bullet_width = 6
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        #Alien Settings
        self.fleet_drop_speed = 8
        
        #How quickly the game speeds up.
        self.speedup_scale = 1.1
        
        # How quickly the alien point value increases.
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        # For settings that change throughout the game.
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.8
        
        # Scoring.
        self.alien_points = 50
        
        # Fleet_direction of 1 represents right; -1 left.
        self.fleet_direction = 1
        
    def increase_speed(self):
        #Increase speed settings with progress.
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)