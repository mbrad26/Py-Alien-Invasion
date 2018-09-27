import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(settings, screen, ship, bullets, bullet_sound, play_button, stats, aliens, alien, sb):
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(play_button, mouse_x, mouse_y, stats, settings, aliens, bullets, alien, ship, screen, sb)


def check_play_button(play_button, mouse_x, mouse_y, stats, settings, aliens, bullets, alien, ship, screen,sb):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        start_game(settings, aliens, bullets, alien, ship, screen, stats, sb)


def start_game(settings, aliens, bullets, alien, ship, screen, stats, sb):
    settings.initialize_settings()
    pygame.mouse.set_visible(False)
    stats.ships_limit = settings.ships_allowed
    stats.game_active = True
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    aliens.empty()
    bullets.empty()
    create_fleet(settings, screen, ship, alien, aliens)
    ship.center = ship.screen_rect.centerx


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


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.rect.right >= alien.screen_rect.right or alien.rect.left <= 0:
            for alien in aliens.sprites():
                alien.rect.y += settings.alien_drop
            settings.change *= -1
            break


def ship_hit(settings, screen, ship, bullets, aliens, alien, stats, sb):
    if stats.ships_limit > 0:
        stats.ships_limit -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, ship, alien, aliens)
        ship.center = ship.screen_rect.centerx
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_alien_bottom(settings, screen, ship, bullets, aliens, stats, sb):
    for alien in aliens.sprites():
        if alien.rect.bottom >= settings.screen_height:
            ship_hit(settings, screen, ship, bullets, aliens, alien, stats, sb)
            break


def update_ship_bullets(settings, ship, bullets, aliens, explosion_sound, stats, sb):
    ship.update()
    bullets.update()
    bullet_update(bullets)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        explosion_sound.play()
        for alien in collisions.values():
            stats.score += settings.alien_points * len(alien)
            sb.prep_score()
        check_high_score(stats, sb)


def update_alien_fleet(settings, screen, ship, bullets, aliens, alien, stats, sb):
    check_edges(settings, aliens)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, screen, ship, bullets, aliens, alien, stats, sb)
    aliens.update()
    check_alien_bottom(settings, screen, ship, bullets, aliens, stats, sb)
    if len(aliens) == 0:
        stats.level += 1
        sb.prep_level()
        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, ship, alien, aliens)
        ship.center = ship.screen_rect.centerx


def draw_screen(settings, screen, ship, bullets, aliens, play_button, stats, sb):
    screen.fill(settings.bg_color)
    # for bullet in bullets.sprites():
    #     bullet.draw_bullet()
    bullets.draw(screen)
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    sb.show_score()
    pygame.display.flip()