# alien_invasion.py

import sys
from time import sleep
import json
from pathlib import Path

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""
    
    def __init__(self):
        """Init the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)      
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
         # Start Alien Invasion in an inactive state.
        self.game_active = (False)
        
        self.play_button = Button(self, "Play")
        
    def _create_fleet(self):    
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    def _create_alien(self, alien_number, row_number):
            alien = Alien(self)
            alien_width, _ = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)
        
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            #Ship hit -1 Lives, and update the scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #Reset aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            #Create new fleets and reset user ship.
            self._create_fleet()
            self.ship.center_ship()        
            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        
    def run_game(self):
        """start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()
        
            # Redraw screen during each pass through loop.       
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
          
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)                      
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            
    def _start_game(self):
         # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            # Reset score
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Gets rid of remaining aliens and bullets.          
            self.aliens.empty()
            self.bullets.empty()
            # Create new alien fleet and center ship.
            self._create_fleet()
            self.ship.center_ship()    
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
                    
    def _check_play_button(self, mouse_pos):
        # Start a new game when the player clicks Play.
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game and start again.
            self.settings.initialize_dynamic_settings()
            self._start_game()
            
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
        elif event.key ==pygame.K_LEFT:
                    self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._close_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # Sets alternative key 'p' to press button.
        elif event.key == pygame.K_p and not self.game_active:
                self._start_game()                
                                
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                    
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
    def _update_bullets(self):
        self.bullets.update()
         # Get rid of bullets that have dissapeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        self._check_bullet_alien_collision()
        
    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
            
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
                
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        #ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        self._check_aliens_bottom()
            
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
                
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        # Draw score information.
        self.sb.show_score()
                 
        # creates new fleet.
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            
         #Draw button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        #Make the most recently drawn screen visable.
        pygame.display.flip()
        
    def _close_game(self):
        """Save high score and exit."""
        saved_high_score = self.stats.get_saved_high_score()
        if self.stats.high_score > saved_high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)
        
        sys.exit()
            
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
    