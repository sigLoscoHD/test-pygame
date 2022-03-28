# Import the pygame module
import pygame

# Import random for random numbers
import random

from model.player import Player
from model.enemy import Enemy

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Goku Ultra Instinct")
background_image = pygame.image.load("assets/background.jpg").convert()

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, and every sprite
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Variable to keep our main loop running
running = True

# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies
    enemies.update()

    # Fill the screen with black
    screen.blit(background_image, [0, 0])

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player and stop the loop
        player.kill()
        running = False

    # Flip everything to the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)