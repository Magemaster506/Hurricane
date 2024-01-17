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

small_shoot_sfx = pygame.mixer.Sound('data/sounds/smallshoot.wav')
big_shoot_sfx = pygame.mixer.Sound('data/sounds/bigshoot.wav')
death_sfx = pygame.mixer.Sound('data/sounds/death.wav')
step1_sfx = pygame.mixer.Sound('data/sounds/step1.mp3')
step2_sfx = pygame.mixer.Sound('data/sounds/step2.mp3')
scrap_pickup_sfx = pygame.mixer.Sound('data/sounds/pickupCoin.wav')
weapon_switch_sfx = pygame.mixer.Sound('data/sounds/weaponswitch.wav')
enemy_hit_sfx = pygame.mixer.Sound('data/sounds/enemyhit.wav')

step1_sfx.set_volume(0.5)
step2_sfx.set_volume(0.5)

footstep_delay = 25
footstep_counter = footstep_delay

scrap_count = 0

coins = []

player_animations = {
    "north": [pygame.image.load(NORTH_FRAME1).convert_alpha(), pygame.image.load(NORTH_FRAME2).convert_alpha(), pygame.image.load(NORTH_FRAME3).convert_alpha(), pygame.image.load(NORTH_FRAME4).convert_alpha()],
    "east": [pygame.image.load(EAST_FRAME1).convert_alpha(), pygame.image.load(EAST_FRAME2).convert_alpha(), pygame.image.load(EAST_FRAME3).convert_alpha(), pygame.image.load(EAST_FRAME4).convert_alpha()],
    "south": [pygame.image.load(SOUTH_FRAME1).convert_alpha(), pygame.image.load(SOUTH_FRAME2).convert_alpha(), pygame.image.load(SOUTH_FRAME3).convert_alpha(), pygame.image.load(SOUTH_FRAME4).convert_alpha()],
    "west": [pygame.image.load(WEST_FRAME1).convert_alpha(), pygame.image.load(WEST_FRAME2).convert_alpha(), pygame.image.load(WEST_FRAME3).convert_alpha(), pygame.image.load(WEST_FRAME4).convert_alpha()],
}
weapon_images = {
    'Pistol': pygame.image.load(PISTOL_IMAGE).convert_alpha(),
    'Machine Gun': pygame.image.load(MACHINE_GUN_IMAGE).convert_alpha(),
    'Shotgun': pygame.image.load(SHOTGUN_IMAGE).convert_alpha(),
}

font = pygame.font.SysFont("arialblack", 40)
TEXT_COL = (255, 255, 255)

def draw_text(text, font, text_col, x, y):
    img = font.renderer(text, True, text_col)
    screen.blit(img, (x, y))

gun_image = pygame.image.load(PISTOL_IMAGE).convert_alpha()

background_image = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
background_pos = [0, 0]

ui_image = pygame.image.load(UI_IMAGE).convert_alpha()

wait_time = 0
screen_shake = 0

player_rect = player_animations[player_direction][player_frame].get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))

clock = pygame.time.Clock()

sparks = []

def main_menu():
    menu_font1 = pygame.font.SysFont("arialblack", 60)
    menu_font2 = pygame.font.SysFont("arialblack", 40)
    menu_text = menu_font1.render("Hurricane", True, (255, 255, 255))
    start_text = menu_font2.render("Press 'Enter' To Start", True, (255, 255, 255))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))  # Fill the screen with a black background
        screen.blit(menu_text, ((WIN_WIDTH - menu_text.get_width()) // 2, (200) // 2))
        screen.blit(start_text, ((WIN_WIDTH - start_text.get_width()) // 2, (500) // 2))

        pygame.display.flip()
        clock.tick(60)

def spawn_enemies(num_enemies, should_spawn = True):
    enemies = []
    if should_spawn:
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
        self.alive = True  # Add an 'alive' attribute
        self.damage = 10

    def apply_screen_shake(self, shake_offset):
        self.position[0] += shake_offset[0]
        self.position[1] += shake_offset[1]

    def decrease_health(self, amount):
        self.health -= amount
        self.hit_flash_timer = 6
        particle_systems.append(EnemyHitParticleSystem([self.position[0], self.position[1]], 2, 4, 3))
        particle_systems.append(SparksParticleSystem([self.position[0], self.position[1]], 1, 8, 1))
        enemy_hit_sfx.play()
        
        if not self.is_alive():
            death_sfx.play()
            coins.append(Coin(self.position[0] + random.uniform(-20, 20), self.position[1] + random.uniform(-20, 20)))
            coins.append(Coin(self.position[0] + random.uniform(-10, 10), self.position[1] + random.uniform(-10, 10)))
            coins.append(Coin(self.position[0] + random.uniform(-10, 10), self.position[1] + random.uniform(-10, 10)))
            trigger_hit_screen_shake(ENEMY_DESTROY_SHAKE_INTENSITY)

    def is_alive(self):
        return self.health > 0 and self.is_alive
    
    def collide_with_player(self, player_position):
        distance = math.sqrt((player_position[0] - self.position[0]) ** 2 + (player_position[1] - self.position[1]) ** 2)
        return distance < self.radius

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

class Door:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Weapon:
    def __init__(self, name, fire_rate, automatic, damage, accuracy, kickback, num_bullets):
        self.name = name
        self.fire_rate = fire_rate
        self.automatic = automatic
        self.damage = damage
        self.accuracy = accuracy
        self.kickback = kickback
        self.num_bullets = num_bullets
        self.shoot_delay = 0
        self.bullets = []

class Coin:
    def __init__(self, x, y):
        self.position = [x, y]
        self.radius = 10
        self.collection_radius = 100
        self.rotation = random.uniform(0, 2 * math.pi)
        self.image = pygame.image.load(random.choice(['data/images/scrap/scrap1.png', 'data/images/scrap/scrap2.png', 'data/images/scrap/scrap3.png'])).convert_alpha()

    def is_collected(self, player_rect):
        coin_rect = pygame.Rect(self.position[0] - self.radius, self.position[1] - self.radius, 2 * self.radius, 2 * self.radius)
        return coin_rect.colliderect(player_rect)
        
    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, math.degrees(self.rotation))
        img_rect = rotated_image.get_rect(center=(self.position[0], self.position[1]))
        screen.blit(rotated_image, img_rect.topleft)

    def update(self, player_position):
        move_speed = 5
        
        dx = player_position[0] - self.position[0]
        dy = player_position[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance > 0 and distance < self.collection_radius:
            move_dx = (dx / distance) * move_speed
            move_dy = (dy / distance) * move_speed
            
            self.position[0] += move_dx
            self.position[1] += move_dy         

pistol = Weapon(name='Pistol', fire_rate = 12, automatic = False, damage = 20, accuracy = 2, kickback = 15, num_bullets = 1)
has_pistol = True
shotgun = Weapon(name='Shotgun', fire_rate = 50, automatic = False, damage = 15, accuracy = 10, kickback = 20, num_bullets = 5)
has_shotgun = True
machine_gun = Weapon(name = 'Machine Gun', fire_rate = 8, automatic = False, damage = 5, accuracy = 5, kickback = 5, num_bullets = 1)
has_machine_gun = True

#starting weapon
current_weapon = pistol

def transition_to_new_scene():
    player_rect.center = (400, 700)
    enemies.clear()
    
    global is_outside
    is_outside = False

def transition_to_old_scene():
    player_rect.center = (400, 100)
    
    global is_outside
    is_outside = True

def check_enemy_collisions(enemies):
    for i, enemy1 in enumerate(enemies):
        for j, enemy2 in enumerate(enemies):
            if i != j and enemy1.is_alive() and enemy2.is_alive():
                distance = math.sqrt((enemy1.position[0] - enemy2.position[0])**2 + (enemy1.position[1] - enemy2.position[1])**2)
                if distance < 2 * enemy1.radius:
                    move_direction = math.atan2(enemy1.position[1] - enemy2.position[1], enemy1.position[0] - enemy2.position[0])
                    move_distance = (2 * enemy1.radius - distance) / 2
                    move_dx = move_distance * math.cos(move_direction)
                    move_dy = move_distance * math.sin(move_direction)
                    enemy2.position[0] -= move_dx
                    enemy2.position[1] -= move_dy
    
main_menu()

enemy = Enemy(0, 0, 20, BASE_ENEMY_HEALTH)  
wave_number = 1
save_wave = 0
enemies = handle_wave(wave_number)
top_door = Door(WIN_WIDTH // 2 - 50, 0, 100, 20)
bottom_door = Door(WIN_WIDTH // 2 - 50, 800, 100, 20)
is_outside = True

while True:
    clock.tick(60)
    wait_time += 1
    player_muzzle_flash_particles = MuzzleFlashParticleSystem([player_rect.centerx, player_rect.centery], 4, 1, 1)    

    if is_outside == True:
        top_door = Door(WIN_WIDTH // 2 - 50, 0, 100, 20)
        if top_door.rect.colliderect(player_rect):
            is_outside = False
            save_wave = wave_number
            transition_to_new_scene()
    else:
        bottom_door = Door(WIN_WIDTH // 2 - 50, 780, 100, 20)
        sparks.clear()
        if bottom_door.rect.colliderect(player_rect):
            is_outside = True
            transition_to_old_scene()
            wave_number = save_wave
        enemies.clear()
        wave_number = save_wave - 1
        
    if player_invincibility_frames > 0:
       player_invincibility_frames -= 1

    if player_health <= 0:
        pygame.quit()
        sys.exit()
    
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

    #base particle settings and handling
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_1 and has_pistol == True and current_weapon is not pistol:
                    current_weapon = pistol
                    weapon_switch_sfx.play()
                    bullets.clear()
                    current_weapon.bullets.clear()
                elif event.key == pygame.K_2 and has_machine_gun == True and current_weapon is not machine_gun:
                    current_weapon = machine_gun
                    weapon_switch_sfx.play()
                    bullets.clear()
                    current_weapon.bullets.clear()
                elif event.key == pygame.K_3 and has_shotgun == True and current_weapon is not shotgun:
                    current_weapon = shotgun
                    weapon_switch_sfx.play()
                    bullets.clear()
                    current_weapon.bullets.clear()
                elif event.key == pygame.K_e:
                    pass

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
        
        footstep_counter -= 1
        if footstep_counter <= 0:
            chosen_footstep_sfx = random.choice([step1_sfx, step2_sfx])
            chosen_footstep_sfx.play()
            footstep_counter = footstep_delay
    else:
        player_frame = 0
    current_frame = player_frame // animation_speed
    player_rect = player_animations[player_direction][current_frame].get_rect(center=player_rect.center)
    
    if is_outside == True:
        if pygame.mouse.get_pressed()[0]:
            if (current_weapon.shoot_delay <= 0):
                if current_weapon == shotgun:
                    big_shoot_sfx.play()
                else:
                    small_shoot_sfx.play()
                for _ in range(current_weapon.num_bullets):
                    random_angle = random.uniform(-current_weapon.accuracy, current_weapon.accuracy)
                    bullet_angle = math.radians(player_angle + random_angle)
                    bullet_pos = [player_rect.centerx + weapon_length * math.cos(bullet_angle),
                                player_rect.centery + weapon_length * math.sin(bullet_angle)]
                    current_weapon.bullets.append([bullet_pos, bullet_angle])
                    particle_systems.append(MuzzleFlashParticleSystem([bullet_pos[0], bullet_pos[1]], 4, 1, 1))
                    gun_kickback = current_weapon.kickback
                    player_rect.x -= gun_kickback_distance * math.cos(bullet_angle)
                    player_rect.y -= gun_kickback_distance * math.sin(bullet_angle)
                current_weapon.shoot_delay = current_weapon.fire_rate  # Convert fire rate to frames
                trigger_hit_screen_shake(HIT_SHAKE_INTENSITY)
            elif not current_weapon.automatic:
                current_weapon.shoot_delay -= 1

    for bullet in current_weapon.bullets:
        bullet_pos, bullet_angle = bullet
        bullet_pos[0] += bullet_speed * math.cos(bullet_angle)
        bullet_pos[1] += bullet_speed * math.sin(bullet_angle)

        for enemy in enemies:
            distance = math.sqrt((bullet_pos[0] - enemy.position[0])**2 + (bullet_pos[1] - enemy.position[1])**2)
            if enemy.is_alive() and bullet not in enemy.hit_bullets:
                if distance < enemy.radius + BULLET_SIZE:
                    enemy.decrease_health(current_weapon.damage)
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

    check_enemy_collisions(enemies)

    for enemy in enemies:
        if enemy.is_alive():
            pygame.draw.circle(screen, (255, 0, 0), (int(enemy.position[0]), int(enemy.position[1])), enemy.radius)
            if enemy.hit_flash_timer > 0:
                pygame.draw.circle(screen, (255, 255, 255), (int(enemy.position[0]), int(enemy.position[1])), enemy.radius)
                
            if player_invincibility_frames == 0:
                for enemy in enemies:
                    if enemy.is_alive():   
                        if enemy.collide_with_player(player_position):
                            trigger_hit_screen_shake(HIT_SHAKE_INTENSITY)
                            player_health -= enemy.damage
                            player_invincibility_frames = invincibility_duration


    screen.blit(player_animations[player_direction][current_frame], player_rect)
    screen.blit(ui_image, background_pos)

    rotated_gun = pygame.transform.rotate(gun_image, -player_angle)
    gun_rect = rotated_gun.get_rect(center=player_rect.center)
    rotated_gun_rect = gun_rect.move(gun_pivot_offset)
    rotated_gun_rect.x -= gun_kickback
    rotated_gun_rect.y -= gun_kickback
    # Replace the existing gun_image line with this block
    if is_outside == True:
        if current_weapon.name in weapon_images:
            gun_image = weapon_images[current_weapon.name]
            rotated_gun = pygame.transform.rotate(gun_image, -player_angle)
            gun_rect = rotated_gun.get_rect(center=player_rect.center)
            rotated_gun_rect = gun_rect.move(gun_pivot_offset)
            rotated_gun_rect.x -= gun_kickback
            rotated_gun_rect.y -= gun_kickback
            screen.blit(rotated_gun, rotated_gun_rect.topleft)

    for bullet in current_weapon.bullets:
        pygame.draw.circle(screen, (255, 255, 255), (int(bullet[0][0]), int(bullet[0][1])), 7.5)


    if not any(enemy.is_alive() for enemy in enemies):
        should_rain = 0
        if wait_time >= WAVE_INTERVAL and is_outside == True:
            wave_number += 1
            enemies = handle_wave(wave_number)

    if any(enemy.is_alive() for enemy in enemies):
        should_rain = 1
    
    if should_rain == 1 and is_outside == True:
        #trigger_hit_screen_shake(1)
        sparks.append(Rain([WIN_WIDTH + 200, -200], math.radians(random.randint(100, 170)), random.randint(20, 30), (255, 255, 255, 1), .5))
        sparks.append(Rain([WIN_WIDTH + 200, -200], math.radians(random.randint(100, 170)), random.randint(40, 50), (255, 255, 255, 1), .2))

    if is_outside == True:
        pygame.draw.rect(screen, (0, 128, 255), top_door.rect)
    else:
        pygame.draw.rect(screen, (0, 128, 255), bottom_door.rect)
        
    for coin in coins:
        coin.update(player_position)
        coin.draw(screen)
        
    for coin in coins[:]:
        if coin.is_collected(player_rect):
            scrap_count += 1
            scrap_pickup_sfx.play()
            particle_systems.append(MuzzleFlashParticleSystem([player_position[0], player_position[1]], 4, 3, 4))
            coins.remove(coin)
        
    pygame.display.flip()

pygame.quit()
