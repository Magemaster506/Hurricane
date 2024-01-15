import pygame
import math
from settings import *
import sys
import random
import time
from rain import Rain

pygame.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

font = pygame.font.SysFont("arialblack", 40)
TEXT_COL = (255, 255, 255)

def draw_text(text, font, text_col, x, y):
    img = font.renderer(text, True, text_col)
    screen.blit(img, (x, y))

player_animations = {
    "north": [pygame.image.load(NORTH_FRAME1).convert_alpha(), pygame.image.load(NORTH_FRAME2).convert_alpha(), pygame.image.load(NORTH_FRAME3).convert_alpha(), pygame.image.load(NORTH_FRAME4).convert_alpha()],
    "east": [pygame.image.load(EAST_FRAME1).convert_alpha(), pygame.image.load(EAST_FRAME2).convert_alpha(), pygame.image.load(EAST_FRAME3).convert_alpha(), pygame.image.load(EAST_FRAME4).convert_alpha()],
    "south": [pygame.image.load(SOUTH_FRAME1).convert_alpha(), pygame.image.load(SOUTH_FRAME2).convert_alpha(), pygame.image.load(SOUTH_FRAME3).convert_alpha(), pygame.image.load(SOUTH_FRAME4).convert_alpha()],
    "west": [pygame.image.load(WEST_FRAME1).convert_alpha(), pygame.image.load(WEST_FRAME2).convert_alpha(), pygame.image.load(WEST_FRAME3).convert_alpha(), pygame.image.load(WEST_FRAME4).convert_alpha()],
}

gun_image = pygame.image.load(PISTOL_IMAGE).convert_alpha()
background_image = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()

ui_image = pygame.image.load(UI_IMAGE).convert_alpha()

wait_time = 0
screen_shake = 0

background_pos = [0, 0]

player_rect = player_animations[player_direction][player_frame].get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))

clock = pygame.time.Clock()

sparks = []

def main_menu():
    menu_font = pygame.font.SysFont("arialblack", 60)
    menu_text = menu_font.render("Your Game Title", True, (255, 255, 255))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.fill((0, 0, 0))  # Fill the screen with a black background
        screen.blit(menu_text, ((WIN_WIDTH - menu_text.get_width()) // 2, (WIN_HEIGHT - menu_text.get_height()) // 2))

        pygame.display.flip()
        clock.tick(60)

main_menu()

def spawn_enemies(num_enemies):
    enemies = []
    for _ in range(num_enemies):
        
        side = random.choice(['top', 'bottom', 'left', 'right'])

        if side == 'top':
            x = random.randint(0, WIN_WIDTH)
            y = random.randint(-100, -50)
        elif side == 'bottom':
            x = random.randint(0, WIN_WIDTH)
            y = random.randint(WIN_HEIGHT + 50, WIN_HEIGHT + 100)
        elif side == 'left':
            x = random.randint(-100, -50)
            y = random.randint(0, WIN_HEIGHT)
        elif side == 'right':
            x = random.randint(WIN_WIDTH + 50, WIN_WIDTH + 100)
            y = random.randint(0, WIN_HEIGHT)

        enemies.append(Enemy(x, y, 20, BASE_ENEMY_HEALTH))
        particle_systems.append(EnemySpawnParticleSystem([x, y], 5, 4, 3))

    return enemies

def handle_wave(wave_number):
        wait_time = 0
        print(f"Wave {wave_number} starting")
        enemies = spawn_enemies(wave_number + wave_number // 2)
        wait_time = 0
        return enemies

def trigger_hit_screen_shake(intensity):
    global screen_shake
    screen_shake = intensity

class SparksParticleSystem:
    def __init__(self, position, num_particles, burst_radius, duration):
        self.particles = []
        self.position = position
        self.num_particles = num_particles
        self.burst_radius = burst_radius
        self.duration = duration

    def spawn_particles(self):
        for _ in range(self.num_particles):
            angle = random.uniform(0, 2 * math.pi / 2)
            speed = random.uniform(1, 3)  # Random speed
            x_speed = speed * math.cos(angle)
            y_speed = speed * math.sin(angle)
            self.particles.append([list(self.position), [x_speed * 2, y_speed * 2], random.randint(2, 4)])

    def update_particles(self):
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= PARTICLE_RANGE  # Particle lifetime
            if particle[2] <= 0 or particle[0][0] < 0 or particle[0][0] > WIN_WIDTH or particle [0][1] < 0 or particle[0][1] > WIN_HEIGHT:
                self.particles.remove(particle)

    def draw_particles(self):
        for particle in self.particles:
            pygame.draw.circle(screen, (255, 255, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
                  
class EnemyHitParticleSystem:
    def __init__(self, position, num_particles, burst_radius, duration):
        self.particles = []
        self.position = position
        self.num_particles = num_particles
        self.burst_radius = burst_radius
        self.duration = duration

    def spawn_particles(self):
        for _ in range(self.num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)  # Random speed
            x_speed = speed * math.cos(angle)
            y_speed = speed * math.sin(angle)
            self.particles.append([list(self.position), [x_speed, y_speed], random.randint(6, 8)])

    def update_particles(self):
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= PARTICLE_RANGE  # Particle lifetime
            if particle[2] <= 0 or particle[0][0] < 0 or particle[0][0] > WIN_WIDTH or particle [0][1] < 0 or particle[0][1] > WIN_HEIGHT:
                self.particles.remove(particle)

    def draw_particles(self):
        for particle in self.particles:
            pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            
class EnemySpawnParticleSystem:
    def __init__(self, position, num_particles, burst_radius, duration):
        self.particles = []
        self.position = position
        self.num_particles = num_particles
        self.burst_radius = burst_radius
        self.duration = duration

    def spawn_particles(self):
        for _ in range(self.num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)  # Random speed
            x_speed = speed * math.cos(angle)
            y_speed = speed * math.sin(angle)
            self.particles.append([list(self.position), [x_speed, y_speed], random.randint(6, 8)])

    def update_particles(self):
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= PARTICLE_RANGE  # Particle lifetime
            if particle[2] <= 0 or particle[0][0] < 0 or particle[0][0] > WIN_WIDTH or particle [0][1] < 0 or particle[0][1] > WIN_HEIGHT:
                self.particles.remove(particle)

    def draw_particles(self):
        for particle in self.particles:
            pygame.draw.circle(screen, (255, 0, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

class MuzzleFlashParticleSystem:
    def __init__(self, position, num_particles, burst_radius, duration):
        self.particles = []
        self.position = position
        self.num_particles = num_particles
        self.burst_radius = burst_radius
        self.duration = duration

    def spawn_particles(self):
        for _ in range(self.num_particles):
            angle = random.uniform(0, 2 * math.pi / 2)
            speed = random.uniform(3, 5)  # Random speed
            x_speed = speed * math.cos(angle)
            y_speed = speed * math.sin(angle)
            self.particles.append([list(self.position), [x_speed, y_speed], random.randint(3, 5)])

    def update_particles(self):
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= MUZZLE_PARTICLE_RANGE  # Particle lifetime
            if particle[2] <= 0 or particle[0][0] < 0 or particle[0][0] > WIN_WIDTH or particle [0][1] < 0 or particle[0][1] > WIN_HEIGHT:
                self.particles.remove(particle)

    def draw_particles(self):
        for particle in self.particles:
            pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

    def update_position(self, position):
            self.position = [position[0], position[1] + 25]

class Enemy:
    def __init__(self, x, y, radius, health):
        self.position = [x, y]
        self.radius = radius
        self.health = health
        self.hit_flash_timer = 0
        self.hit_bullets = []  

    def apply_screen_shake(self, shake_offset):
        self.position[0] += shake_offset[0]
        self.position[1] += shake_offset[1]

    def decrease_health(self, amount):
        self.health -= amount
        self.hit_flash_timer = 6
        particle_systems.append(EnemyHitParticleSystem([self.position[0], self.position[1]], 2, 4, 3))
        particle_systems.append(SparksParticleSystem([self.position[0], self.position[1]], 1, 8, 1))
        
        if not self.is_alive():
            trigger_hit_screen_shake(ENEMY_DESTROY_SHAKE_INTENSITY)

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
    
enemy = Enemy(0, 0, 20, BASE_ENEMY_HEALTH)  
wave_number = 1
enemies = handle_wave(wave_number)

while True:
    clock.tick(60)
    wait_time += 1
    player_muzzle_flash_particles = MuzzleFlashParticleSystem([player_rect.centerx, player_rect.centery], 4, 1, 1)
    if screen_shake > 0:
        shake_offset = (random.randint(-screen_shake, screen_shake), random.randint(-screen_shake, screen_shake))
        enemy_shake_offset = (random.randint(-screen_shake, screen_shake), random.randint(-screen_shake, screen_shake))
        screen.blit(background_image, (background_pos[0] + shake_offset[0], background_pos[1] + shake_offset[1]))

        player_rect = player_animations[player_direction][current_frame].get_rect(
            center=(player_rect.centerx + shake_offset[0], player_rect.centery + shake_offset[1]))

        for enemy in enemies:
            enemy.apply_screen_shake(enemy_shake_offset)
        
        screen_shake -= 1
    else:
        screen.blit(background_image, background_pos)
    
    for i, spark in sorted(enumerate(sparks), reverse=True):
        spark.move(1)
        spark.draw(screen)
        if not spark.alive:
            sparks.pop(i)

    #static particle settings and handling
    for system in particle_systems:
        if system.duration > 0:
            system.spawn_particles()
            system.duration -= 1
        system.update_particles()
        system.draw_particles()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

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
            particle_systems.append(MuzzleFlashParticleSystem([bullet_pos[0], bullet_pos[1]], 4, 1 , 1))
            gun_kickback = gun_kickback_distance
            player_rect.x -= gun_kickback_distance * math.cos(bullet_angle)
            player_rect.y -= gun_kickback_distance * math.sin(bullet_angle)
            shoot_delay = 10
            trigger_hit_screen_shake(HIT_SHAKE_INTENSITY)
        else:
            shoot_delay -= 1

    for bullet in bullets:
        bullet_pos, bullet_angle = bullet
        bullet_pos[0] += bullet_speed * math.cos(bullet_angle)
        bullet_pos[1] += bullet_speed * math.sin(bullet_angle)

        for enemy in enemies:
            distance = math.sqrt((bullet_pos[0] - enemy.position[0])**2 + (bullet_pos[1] - enemy.position[1])**2)
            if enemy.is_alive() and bullet not in enemy.hit_bullets:
                if distance < enemy.radius + BULLET_SIZE:
                    enemy.decrease_health(10)
                    wait_time = 0
                    knockback_distance = ENEMY_KNOCKBACK  
                    knockback_direction = math.radians(player_angle) 
                    enemy.position[0] += knockback_distance * math.cos(knockback_direction)
                    enemy.position[1] += knockback_distance * math.sin(knockback_direction)
                 
                    enemy.hit_bullets.append(bullet)
                    trigger_hit_screen_shake(HIT_SHAKE_INTENSITY)

    if gun_kickback > 0:
        gun_kickback -= gun_kickback_speed
    else:
        gun_kickback = 0

    for enemy in enemies:
        enemy.update(player_position)

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
        should_rain = 0
        if wait_time >= WAVE_INTERVAL:
            wave_number += 1
            enemies = handle_wave(wave_number)

    if any(enemy.is_alive() for enemy in enemies):
        should_rain = 1
        check = random.randint(0,5)
    
    if should_rain == 1:
        sparks.append(Rain([WIN_WIDTH + 200, -200], math.radians(random.randint(100, 170)), random.randint(20, 30), (255, 255, 255, 1), .5))
        sparks.append(Rain([WIN_WIDTH + 200, -200], math.radians(random.randint(100, 170)), random.randint(40, 50), (255, 255, 255, 1), .2))

    if moving:
        player_muzzle_flash_particles.update_position([player_rect.centerx, player_rect.centery])
        player_muzzle_flash_particles.spawn_particles()

    # Update and draw particles
    player_muzzle_flash_particles.update_particles()
    player_muzzle_flash_particles.draw_particles()

    pygame.display.flip()



pygame.quit()