#bullet.py

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #Bullet class
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        #Creates a bullet at (0, 0) and then set position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #Store the bullets pos as a dec value.
        self.y = float(self.rect.y)
        
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
        
    def update(self):
        # update dec pos of the bullet.
        self.y -= self.settings.bullet_speed
        # update the rect  pos.
        self.rect.y = self.y
        
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
        