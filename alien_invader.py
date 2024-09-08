import math
import random
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Sound
mixer.music.load("music.mp3")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = WIDTH // 2
playerY = HEIGHT - 100
playerX_change = 0
playerY_change = 0
player_speed = 5

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemySpeed = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(f'ships/ship ({i+1}).png'))
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (64, 64))
    enemyX.append(random.randint(0, WIDTH - 64))
    enemyY.append(random.randint(50, 200))
    enemySpeed.append(0.5)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 0
bulletSpeed = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (WIDTH//2 - 200, HEIGHT//2 - 32))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    return distance < 27


# Game Loop
clock = pygame.time.Clock()
running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_speed
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed
            if event.key == pygame.K_UP:
                playerY_change = -player_speed
            if event.key == pygame.K_DOWN:
                playerY_change = player_speed
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                bulletX = playerX
                bulletY = playerY
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                playerY_change = 0

    # Player movement
    playerX += playerX_change
    playerY += playerY_change

    # Enemy movement
    for i in range(num_of_enemies):
        # Move towards player
        dx = playerX - enemyX[i]
        dy = playerY - enemyY[i]
        dist = math.sqrt(dx**2 + dy**2)
        if dist != 0:
            enemyX[i] += (dx / dist) * enemySpeed[i]
            enemyY[i] += (dy / dist) * enemySpeed[i]

        # Game Over
        if math.sqrt((playerX - enemyX[i])**2 + (playerY - enemyY[i])**2) < 50:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Collision
        if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            # play the explosion image
        
            bulletY = playerY
            # change the enemy image to explosion
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, WIDTH - 64)
            enemyY[i] = random.randint(50, 200)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletSpeed

    # Simulate forward movement
    for i in range(num_of_enemies):
        enemyY[i] += 0.05
        if enemyY[i] > HEIGHT:
            enemyX[i] = random.randint(0, WIDTH - 64)
            enemyY[i] = random.randint(-100, -50)

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
