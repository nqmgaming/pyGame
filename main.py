import pygame
from os.path import join
from random import randint, choice

# General setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()
font_path = join("images", "Oxanium-Bold.ttf")
font = pygame.font.Font(font_path, 40)

# Load sounds
damage_sound = pygame.mixer.Sound(join("audio", "damage.ogg"))
explosion_sound = pygame.mixer.Sound(join("audio", "explosion.wav"))
laser_sound = pygame.mixer.Sound(join("audio", "laser.wav"))
pygame.mixer.music.load(join("audio", "game_music.wav"))

# Play background music
pygame.mixer.music.play(-1)  # Loop indefinitely

# Game Variables
player_lives = 3
game_active = False
score = 0
invincible_time = 0
invincible_duration = 3000

# Importing images
player_surf = pygame.image.load(join("images", "player.png")).convert_alpha()
player_rect = player_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))

meteor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()
meteor_list = []

laser_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()
laser_list = []

star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH - star_surf.get_width()), randint(0, WINDOW_HEIGHT - star_surf.get_height()))
                  for _ in range(20)]

# Load explosion images
explosion_images = [pygame.image.load(join("images/explosion", f"{i}.png")).convert_alpha() for i in range(21)]
explosions = []

# Player movement setup
player_speed = 10

# Meteor movement setup
meteor_speed = 5
meteor_horizontal_speed = 2


# Functions
def create_meteor():
    meteor_rect = meteor_surf.get_rect(center=(randint(0, WINDOW_WIDTH), randint(-100, -50)))
    return meteor_rect


def move_meteors():
    global meteor_horizontal_speed
    for meteor_rect in meteor_list:
        meteor_rect.y += meteor_speed
        meteor_rect.x += choice([-1, 0, 1]) * meteor_horizontal_speed  # Di chuyển ngang

        # Đảm bảo thiên thạch không ra ngoài màn hình
        if meteor_rect.left < 0:
            meteor_rect.left = 0
        if meteor_rect.right > WINDOW_WIDTH:
            meteor_rect.right = WINDOW_WIDTH

        if meteor_rect.top > WINDOW_HEIGHT:
            meteor_list.remove(meteor_rect)
            meteor_list.append(create_meteor())  # Thay thế thiên thạch khi ra khỏi màn hình


def fire_laser():
    laser_rect = laser_surf.get_rect(midbottom=player_rect.midtop)
    laser_list.append(laser_rect)
    laser_sound.play()


def move_lasers():
    for laser_rect in laser_list:
        laser_rect.y -= 10
        if laser_rect.bottom < 0:
            laser_list.remove(laser_rect)


def check_collisions():
    global player_lives, game_active, score, invincible_time

    # Kiểm tra va chạm giữa người chơi và thiên thạch
    if invincible_time <= pygame.time.get_ticks():
        for meteor_rect in meteor_list:
            if player_rect.colliderect(meteor_rect):
                player_lives -= 1
                damage_sound.play()
                meteor_list.remove(meteor_rect)
                meteor_list.append(create_meteor())
                if player_lives == 0:
                    game_active = False
                else:
                    invincible_time = pygame.time.get_ticks() + invincible_duration  # Bắt đầu thời gian bất tử

    # Kiểm tra va chạm giữa laser và thiên thạch
    for meteor_rect in meteor_list:
        for laser_rect in laser_list:
            if laser_rect.colliderect(meteor_rect):
                explosion_sound.play()
                explosions.append((meteor_rect.center, 0))  # Start explosion animation
                meteor_list.remove(meteor_rect)
                laser_list.remove(laser_rect)
                meteor_list.append(create_meteor())
                score += 10
                break


def display_score():
    score_surf = font.render(f'Score: {score}', True, (255, 255, 255))
    display_surface.blit(score_surf, (WINDOW_WIDTH - 200, 10))


def animate_explosions():
    for explosion in explosions:
        pos, frame = explosion
        display_surface.blit(explosion_images[frame], explosion_images[frame].get_rect(center=pos))
        if frame < len(explosion_images) - 1:
            explosions[explosions.index(explosion)] = (pos, frame + 1)
        else:
            explosions.remove(explosion)


def display_lives():
    lives_surf = font.render(f'Lives: {player_lives}', True, (255, 255, 255))
    display_surface.blit(lives_surf, (10, 10))


def display_menu():
    display_surface.fill((0, 0, 0))
    title_surf = font.render('Space Shooter', True, (255, 255, 255))
    start_surf = font.render('Press SPACE to Start', True, (255, 255, 255))
    quit_surf = font.render('Press Q to Quit', True, (255, 255, 255))
    display_surface.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, WINDOW_HEIGHT // 3))
    display_surface.blit(start_surf, (WINDOW_WIDTH // 2 - start_surf.get_width() // 2, WINDOW_HEIGHT // 2))
    display_surface.blit(quit_surf, (WINDOW_WIDTH // 2 - quit_surf.get_width() // 2, WINDOW_HEIGHT // 2 + 100))


def draw_player():
    if invincible_time > pygame.time.get_ticks():
        # Nhấp nháy người chơi
        if pygame.time.get_ticks() % 500 < 250:  # Thay đổi tần suất nhấp nháy nếu cần
            return
    display_surface.blit(player_surf, player_rect)


# Game Loop
while True:
    clock.tick(60)

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fire_laser()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    player_lives = 3
                    meteor_list = [create_meteor() for _ in range(5)]
                    laser_list.clear()
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
            player_rect.y += player_speed

        move_meteors()
        move_lasers()
        check_collisions()

        display_surface.fill((0, 0, 0))
        for pos in star_positions:
            display_surface.blit(star_surf, pos)
        draw_player()  # Sử dụng hàm vẽ người chơi
        for meteor_rect in meteor_list:
            display_surface.blit(meteor_surf, meteor_rect)
        for laser_rect in laser_list:
            display_surface.blit(laser_surf, laser_rect)

        animate_explosions()
        display_lives()
        display_score()
    else:
        display_menu()

    pygame.display.update()

pygame.quit()
