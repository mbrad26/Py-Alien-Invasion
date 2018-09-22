import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(settings, screen, ship, bullets, bullet_sound):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            if event.key == pygame.K_LEFT:
                ship.moving_left = True
            if event.key == pygame.K_SPACE:
                if len(bullets) < settings.bullets_allowed:
                    new_bullet = Bullet(settings, screen, ship)
                    bullets.add(new_bullet)
                    bullet_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            if event.key == pygame.K_LEFT:
                ship.moving_left = False


def create_fleet(settings, screen, ship, alien, aliens):
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height
    available_space_x = settings.screen_width - (2 * alien_width)
    available_space_y = settings.screen_height - (3 * alien_height) - ship_height
    aliens_per_row = int(available_space_x / (2 * alien_width))
    rows = int(available_space_y / (2 * alien_height))
    for row in range(rows):
        for a in range(aliens_per_row):
            alien = Alien(settings, screen)
            alien.x = alien_width + 2 * alien_width * a
            alien.rect.x = alien.x
            alien.y = alien_height + 2 * alien_height * row
            alien.rect.y = alien.y
            aliens.add(alien)


def bullet_update(bullets):
    for bullet in bullets.sprites():
        if bullet.rect.bottom < 0:
            bullet.kill()


def update_ship_bullets(ship, bullets, aliens, explosion_sound):
    ship.update()
    bullets.update()
    bullet_update(bullets)
    if pygame.sprite.groupcollide(bullets, aliens, True, True):
        explosion_sound.play()


def check_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.rect.right >= alien.screen_rect.right or alien.rect.left <= 0:
            for alien in aliens.sprites():
                alien.rect.y += settings.alien_drop
            settings.change *= -1
            break


def ship_hit(settings, screen, ship, bullets, aliens, alien, stats):
    if stats.ships_limit > 0:
        stats.ships_limit -= 1
        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, ship, alien, aliens)
        ship.center = ship.screen_rect.centerx
        sleep(0.5)
    else:
        stats.game_active = False


def check_alien_bottom(settings, screen, ship, bullets, aliens, stats):
    for alien in aliens.sprites():
        if alien.rect.bottom >= settings.screen_height:
            ship_hit(settings, screen, ship, bullets, aliens, alien, stats)
            break


def update_alien_fleet(settings, screen, ship, bullets, aliens, alien, stats):
    check_edges(settings, aliens)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, screen, ship, bullets, aliens, alien, stats)
    aliens.update()
    check_alien_bottom(settings, screen, ship, bullets, aliens, stats)


def draw_screen(settings, screen, ship, bullets, aliens):
    screen.fill(settings.bg_color)
    # for bullet in bullets.sprites():
    #     bullet.draw_bullet()
    bullets.draw(screen)
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()