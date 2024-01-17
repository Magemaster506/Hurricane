import pygame
import sys

pygame.init()

# Define your constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MENU_WIDTH = 200
MENU_HEIGHT = 300

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Overlay Menu")

clock = pygame.time.Clock()

class Menu:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.buttons = []

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        for button in self.buttons:
            pygame.draw.rect(screen, BLACK, button)

# Initialize menu
menu = Menu(SCREEN_WIDTH - MENU_WIDTH, 0, MENU_WIDTH, SCREEN_HEIGHT)
menu.buttons = [
    pygame.Rect(SCREEN_WIDTH - MENU_WIDTH + 20, 50, 160, 40),
    pygame.Rect(SCREEN_WIDTH - MENU_WIDTH + 20, 120, 160, 40),
]

player_x, player_y = 100, 100
player_speed = 5
menu_open = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu_open = not menu_open

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not menu_open:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and not menu_open:
        player_x += player_speed
    if keys[pygame.K_UP] and not menu_open:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and not menu_open:
        player_y += player_speed

    # Clear the screen
    screen.fill(BLACK)

    # Draw the player
    pygame.draw.rect(screen, WHITE, (player_x, player_y, 50, 50))

    # Draw the menu if it's open
    if menu_open:
        menu.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
