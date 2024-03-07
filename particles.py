import random
import math
import pygame
from settings import *

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