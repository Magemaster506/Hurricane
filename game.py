import pygame
import math
from settings import *
import sys
import random
import time

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(WIN_TITLE)

class Enemy:
    def __init__(self, x, y, radius, health):
        self.position = [x, y]
        self.radius = radius
        self.health = health
        self.hit_flash_timer = 0
        self.hit_bullets = []  

    def decrease_health(self, amount):
        self.health -= amount
        self.hit_flash_timer = 6  

    def is_alive(self):
        return self.health > 0

    def update(self, player_position):
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1
            
        if self.is_alive():
            dx = player_position[0] - self.position[0]
            dy = player_position[1] - self.position[1]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                move_speed = BASE_ENEMY_MOVE_SPEED
                move_dx = (dx / distance) * move_speed
                move_dy = (dy / distance) * move_speed
                
                self.position[0] += move_dx
                self.position[1] += move_dy

player_animations = {
    "north": [pygame.image.load(NORTH_FRAME1), pygame.image.load(NORTH_FRAME2), pygame.image.load(NORTH_FRAME3), pygame.image.load(NORTH_FRAME4)],
    "east": [pygame.image.load(EAST_FRAME1), pygame.image.load(EAST_FRAME2), pygame.image.load(EAST_FRAME3), pygame.image.load(EAST_FRAME4)],
    "south": [pygame.image.load(SOUTH_FRAME1), pygame.image.load(SOUTH_FRAME2), pygame.image.load(SOUTH_FRAME3), pygame.image.load(SOUTH_FRAME4)],
    "west": [pygame.image.load(WEST_FRAME1), pygame.image.load(WEST_FRAME2), pygame.image.load(WEST_FRAME3), pygame.image.load(WEST_FRAME4)],
}

gun_image = pygame.image.load(PISTOL_IMAGE)
background_image = pygame.image.load(BACKGROUND_IMAGE)

ui_image = pygame.image.load(UI_IMAGE)

background_pos = [0, 0]

player_direction = "south"
player_frame = 0
player_rect = player_animations[player_direction][player_frame].get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
player_speed = PLAYER_SPEED
animation_speed = 8

weapon_length = 55
gun_pivot_offset = (-5, 10)
gun_kickback_distance = 4
gun_kickback_speed = 2
gun_kickback = 0

shoot_delay = FIRE_RATE
bullet_accuracy = BULLET_ACCURACY
bullet_speed = BULLET_TRAVEL_SPEED

bullets = []

enemy = Enemy(800, 800, 20, BASE_ENEMY_HEALTH)  

clock = pygame.time.Clock()

def spawn_enemies(num_enemies):
    enemies = []
    num_enemies = 5
    for _ in range(num_enemies):
        x = random.randint(50, WIN_WIDTH - 50)
        y = random.randint(50, WIN_HEIGHT - 50)
        print(f"enemypos: ({x}, {y})")
        enemies.append(Enemy(x, y, 20, BASE_ENEMY_HEALTH))
    return enemies

def handle_wave(wave_number):
    print(f"Wave {wave_number} starting")
    enemies = spawn_enemies(wave_number * 2)
    print(f"Number of enemies: {len(enemies)}")
    return enemies

wave_number = 1
enemies = handle_wave(wave_number)

run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.K_ESCAPE:
            run = False


    player_position = [player_rect.centerx, player_rect.centery]
    mouse_x, mouse_y = pygame.mouse.get_pos()

    dx = mouse_x - player_rect.centerx
    dy = mouse_y - player_rect.centery
    player_angle = math.degrees(math.atan2(dy, dx))

    if abs(dy) > abs(dx):
        if dy < 0:
            player_direction = "north"
        else:
            player_direction = "south"
    else:
        if dx > 0:
            player_direction = "east"
        else:
            player_direction = "west"

    keys = pygame.key.get_pressed()
    moving = False

    if keys[pygame.K_a] and not keys[pygame.K_d]:
        player_rect.move_ip(-player_speed, 0)
        moving = True
    elif keys[pygame.K_d] and not keys[pygame.K_a]:
        player_rect.move_ip(player_speed, 0)
        moving = True

    if keys[pygame.K_w] and not keys[pygame.K_s]:
        player_rect.move_ip(0, -player_speed)
        moving = True
    elif keys[pygame.K_s] and not keys[pygame.K_w]:
        player_rect.move_ip(0, player_speed)
        moving = True

    if moving:
        player_frame = (player_frame + 1) % (len(player_animations[player_direction]) * animation_speed)
    else:
        player_frame = 0
    current_frame = player_frame // animation_speed
    player_rect = player_animations[player_direction][current_frame].get_rect(center=player_rect.center)

    if pygame.mouse.get_pressed()[0]:
        if shoot_delay <= 0:
            random_angle = random.uniform(-bullet_accuracy, bullet_accuracy)
            bullet_angle = math.radians(player_angle + random_angle)
            bullet_pos = [player_rect.centerx + weapon_length * math.cos(bullet_angle),
                          player_rect.centery + weapon_length * math.sin(bullet_angle)]
            bullets.append([bullet_pos, bullet_angle])
            gun_kickback = gun_kickback_distance
            player_rect.x -= gun_kickback_distance * math.cos(bullet_angle)
            player_rect.y -= gun_kickback_distance * math.sin(bullet_angle)
            shoot_delay = 10
        else:
            shoot_delay -= 1

    for bullet in bullets:
        bullet_pos, bullet_angle = bullet
        bullet_pos[0] += bullet_speed * math.cos(bullet_angle)
        bullet_pos[1] += bullet_speed * math.sin(bullet_angle)

        # Check for collision with enemies and update their health
        for enemy in enemies:
            distance = math.sqrt((bullet_pos[0] - enemy.position[0])**2 + (bullet_pos[1] - enemy.position[1])**2)
            if enemy.is_alive() and bullet not in enemy.hit_bullets:
                if distance < enemy.radius + 7.5:
                    enemy.decrease_health(10)

                    knockback_distance = ENEMY_KNOCKBACK  
                    knockback_direction = math.radians(player_angle) 
                    enemy.position[0] += knockback_distance * math.cos(knockback_direction)
                    enemy.position[1] += knockback_distance * math.sin(knockback_direction)
                 
                    enemy.hit_bullets.append(bullet)

                    if not enemy.is_alive():
                        bullets.remove(bullet)

    if gun_kickback > 0:
        gun_kickback -= gun_kickback_speed
    else:
        gun_kickback = 0

    # Update enemy positions
    for enemy in enemies:
        enemy.update(player_position)

    screen.blit(background_image, background_pos)

    for enemy in enemies:
        if enemy.is_alive():
            pygame.draw.circle(screen, (255, 0, 0), (int(enemy.position[0]), int(enemy.position[1])), enemy.radius)
            if enemy.hit_flash_timer > 0:
                pygame.draw.circle(screen, (255, 255, 255), (int(enemy.position[0]), int(enemy.position[1])), enemy.radius)

    screen.blit(player_animations[player_direction][current_frame], player_rect)
    screen.blit(ui_image, background_pos)

    rotated_gun = pygame.transform.rotate(gun_image, -player_angle)
    gun_rect = rotated_gun.get_rect(center=player_rect.center)
    rotated_gun_rect = gun_rect.move(gun_pivot_offset)
    rotated_gun_rect.x -= gun_kickback
    rotated_gun_rect.y -= gun_kickback
    screen.blit(rotated_gun, rotated_gun_rect.topleft)

    for bullet in bullets:
        pygame.draw.circle(screen, (255, 255, 255), (int(bullet[0][0]), int(bullet[0][1])), 7.5)

    if not any(enemy.is_alive() for enemy in enemies):
        wave_number += 1
        enemies = handle_wave(wave_number)

    pygame.display.flip()

pygame.quit()
