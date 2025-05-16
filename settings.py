class Settings:
    
    def __init__(self):
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        #Ship Settings
        self.ship_speed = 1.5
        self.ship_limit = 1
        
        #Bullets
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        #Alien Settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # Fleet_direction of 1 represents right; -1 left.
        self.fleet_direction = 1