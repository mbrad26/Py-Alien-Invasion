import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from gamestats import Stats
from button import Button
from scoreboard import Scoreboard


def run_game():

    pygame.init()
    pygame.mixer.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Alien')
    play_button = Button(settings, screen, 'Play')

    bullet_sound = pygame.mixer.Sound('sounds/Laser_Shoot16.ogg')
    explosion_sound = pygame.mixer.Sound('sounds/Explosion20.wav')

    ship = Ship(settings, screen)
    alien = Alien(settings, screen)
    stats = Stats(settings)
    sb = Scoreboard(settings, screen, stats)

    bullets = Group()
    aliens = Group()

    # Create alien fleet
    gf.create_fleet(settings, screen, ship, alien, aliens)

    while True:

        # Events
        gf.check_events(settings, screen, ship, bullets, bullet_sound, play_button, stats, aliens, alien, sb)

        # Updates
        if stats.game_active:
            gf.update_ship_bullets(settings, ship, bullets, aliens, explosion_sound, stats, sb)
            gf.update_alien_fleet(settings, screen, ship, bullets, aliens, alien, stats, sb)

        # Draw
        gf.draw_screen(settings, screen, ship, bullets, aliens, play_button, stats, sb)


run_game()