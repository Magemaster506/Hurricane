import random
import math
import pygame
from settings import *

sparks2 = []

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
           # pygame.draw.polygon(surf, self.color, points)
            pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

    def update_position(self, position):
            self.position = [position[0], position[1] + 25]

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
            speed = random.uniform(3, 6)  # Random speed
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
            
            
class Polygon():
    def __init__(self, loc, angle, speed, color, scale=10):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sing = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]


    # gravity and friction
    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])
        # if you want to get more realistic, the speed should be adjusted here

    def move(self, dt):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        # a bunch of options to mess around with relating to angles...
        #self.point_towards(math.pi / 2, 0.02)
        #self.velocity_adjust(0.975, 0.2, 8, dt)
        #self.angle += 0.1

        self.speed -= 0.1

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf, offset=[0, 0]):
        points = [
            [self.loc[0] + math.cos(self.angle) * self.speed * self.scale, self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
            [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
            [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
            [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
            ]
        pygame.draw.polygon(surf, self.color, points)
    