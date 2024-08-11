import pygame
from os.path import join
from random import randint

# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True

# Importing images
player_surf = pygame.image.load(join("images", "player.png")).convert_alpha()
player_rect = player_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

meteor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()
meteor_rect = meteor_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))  # Moved meteor position

laser_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()
laser_rect = laser_surf.get_rect(bottomleft=(20, WINDOW_HEIGHT - 70))

star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
star_positions = []
for _ in range(20):
    star_x = randint(0, WINDOW_WIDTH - star_surf.get_width())
    star_y = randint(0, WINDOW_HEIGHT - star_surf.get_height())
    star_positions.append((star_x, star_y))

# Player speed
player_speed = 0.4
player_position = float(player_rect.x)

# Player direction
player_direction = 1


while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update player position
    player_position += player_direction * player_speed
    player_rect.x = int(player_position)

    if player_rect.right >= WINDOW_WIDTH or player_rect.left <= 0:
        player_direction *= -1

    # Draw the game
    display_surface.fill((169, 169, 169))
    for pos in star_positions:
        display_surface.blit(star_surf, pos)
    display_surface.blit(player_surf, player_rect)
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    pygame.display.update()

pygame.quit()
