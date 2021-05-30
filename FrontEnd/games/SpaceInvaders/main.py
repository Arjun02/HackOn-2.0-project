# Based on Code Camp tutorial

import pygame
import math
import random

# Creates a "pygame"
pygame.init()

# Creates the window
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption('Space Invaders')

icon = pygame.image.load('space-invaders-32.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Score and Game Over
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Player - player() - location updater
playerImg = pygame.image.load('space-invaders-64.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy - enemy() - location updater
enemyImg = pygame.image.load('pixelated-alien.png')
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = 20
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)


def enemy(x, y, i):
    screen.blit(enemyImg, (x, y))


# Bullet - ready, not on screen. fire, bullet is moving - bullet() - location updater
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Collision mechanics
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True


# Game loop
operation = True
while operation:
    # RGB Background
    screen.fill((125, 125, 125))
    screen.blit(background, (0, 0))

    # Exit button function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            operation = False

    # Key detection
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5
        if event.key == pygame.K_LCTRL:
            if bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    # Player location and boundaries
    playerX += playerX_change
    if playerX > 736:
        playerX = 736
    elif playerX < 0:
        playerX = 0

    # Enemy navigation and boundaries
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 250:
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change
        elif enemyX[i] < 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change

        # Collision detection
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

print("done")