import random
import math
import pygame
from settings import *
from particles import *
from sounds import *

def trigger_hit_screen_shake(intensity):
    global screen_shake
    screen_shake = intensity

class Coin:
    def __init__(self, x, y):
        self.position = [x, y]
        self.radius = 10
        self.collection_radius = COIN_COLLECTION_RANGE
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

class Enemy:
    def __init__(self, x, y, radius, health):
        self.position = [x, y]
        self.radius = radius
        self.health = health
        self.hit_flash_timer = 0
        self.hit_bullets = []  
        self.alive = True
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
            scrap_amount = random.randint(1, 5)
            for _ in range(scrap_amount):
                coins.append(Coin(self.position[0] + random.uniform(-20, 20), self.position[1] + random.uniform(-20, 20)))
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