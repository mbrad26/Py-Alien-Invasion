import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from gamestats import Stats


def run_game():

    pygame.init()
    pygame.mixer.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Alien')

    bullet_sound = pygame.mixer.Sound('sounds/Laser_Shoot16.ogg')
    explosion_sound = pygame.mixer.Sound('sounds/Explosion20.wav')

    ship = Ship(settings, screen)
    alien = Alien(settings, screen)
    stats = Stats(settings)

    bullets = Group()
    aliens = Group()

    # Create alien fleet
    gf.create_fleet(settings, screen, ship, alien, aliens)

    while True:

        # Events
        gf.check_events(settings, screen, ship, bullets, bullet_sound)

        # Updates
        if stats.game_active:
            gf.update_ship_bullets(ship, bullets, aliens, explosion_sound)
            gf.update_alien_fleet(settings, screen, ship, bullets, aliens, alien, stats)

            print('Stats ' + str(stats.ships_limit))
        # Draw
        gf.draw_screen(settings, screen, ship, bullets, aliens)


run_game()