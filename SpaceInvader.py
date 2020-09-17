import pygame
import random
import math

# Initialize the pygame
pygame.init()
from pygame import mixer

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# BackGround Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Game Title & Logo
pygame.display.set_caption("Space Assault")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 500
playerX_change = 0

# Monster
monsterImg = []
monsterX = []
monsterY = []
monsterX_change = []
monsterY_change = []
num_of_monsters = 6

for i in range(num_of_monsters):
    monsterImg.append(pygame.image.load('monster.png'))
    monsterX.append(random.randint(0, 735))
    monsterY.append(random.randint(50, 150))
    monsterX_change.append(1.5)
    monsterY_change.append(40)

# Laser
# Ready - Cant see the laser on screen
# Fire - The laser currently moves
laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 5
laser_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def monster(x, y, i):
    screen.blit(monsterImg[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


def isCollision(monsterX, monsterY, laserX, laserY):
    distance = math.sqrt((math.pow(monsterX - laserX, 2)) + (math.pow(monsterY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checks if keystroke is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = +5
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Boundary of space ship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 736
    elif playerX >= 736:
        playerX = 0

        # Monsters movement
    for i in range(num_of_monsters):

        # Game Over
        if monsterY[i] > 438:
            for j in range(num_of_monsters):
                monsterY[j] = 20000
            game_over_text()
            break

        monsterX[i] += monsterX_change[i]
        if monsterX[i] <= 0:
            monsterY[i] += monsterY_change[i]
            monsterX_change[i] = 1.5
        elif monsterX[i] >= 736:
            monsterX_change[i] = -1.5
            monsterY[i] += monsterY_change[i]

        # Collision
        collision = isCollision(monsterX[i], monsterY[i], laserX, laserY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            laserY = 480
            laser_state = "ready"
            score_value += 1
            monsterX[i] = random.randint(0, 735)
            monsterY[i] = random.randint(50, 150)

        monster(monsterX[i], monsterY[i], i)

    # Laser Movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
