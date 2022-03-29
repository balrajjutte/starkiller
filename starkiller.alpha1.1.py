import pygame
import math
import random

# initalise the pygame
pygame.init()

# create the screen (W, H)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("images/background.png")

# Title and Icon (32pxlby32pxl)
pygame.display.set_caption("Starkiller")
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)


# Collison Function
class Collision():
    @staticmethod
    def isCollision(x1, y1, x2, y2):
        distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
        if distance < 27:
            return True
        return False

    @staticmethod
    def BulletCollison():
        global bullet_state, score_value
        bullet_state = 'ready'
        score_value += 1

    @staticmethod
    def PlayerCollsion(x1, y1, x2, y2):
        global health_value, running
        isCollision = Collision.isCollision(x1, y1, x2, y2)
        print(health_value)
        if isCollision:
            health_value -= 10
            if health_value == 0:
                running = False


# MAIN Class
class Main:
    def __init__(self, x, y, x_del, y_del, img):
        self.x = x
        self.y = y
        self.x_del = x_del
        self.y_del = y_del
        self.img = img

    def Display(self, x, y, img):
        screen.blit(img, (x, y))

    def KeydownEvents(self, x_del, y_del):

        if event.key == pygame.K_LEFT:
            x_del = -7
        if event.key == pygame.K_RIGHT:
            x_del = 7
        if event.key == pygame.K_UP:
            y_del = -7
        if event.key == pygame.K_DOWN:
            y_del = 7
        return x_del, y_del

    def KeyupEvents(self, x_del, y_del):
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            x_del = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            y_del = 0
        return x_del, y_del


# PLayer Class
class Player(Main):
    def PlayerMovement(self, x, y, x_del, y_del):
        x += x_del
        y += y_del
        if x <= 0:
            x = 0
        elif x >= 736:
            x = 736
        if y <= 0:
            y = 0
        elif y >= 536:
            y = 536
        return x, y


# Bullet Class
class Bullet(Main):
    def __init__(self, x, y, x_del, y_del, img, state):
        super().__init__(x, y, x_del, y_del, img)
        self.state = state

    def FireBullet(self, x, y):
        state = "fire"
        screen.blit(bulletIMG, (x + 16, y + 10))
        return state

    def BulletMovement(self, x, y, y_del, state):
        if y <= 0:
            y = 480
            state = 'ready'
        if state == 'fire':
            state = self.FireBullet(x, y)
            y -= y_del
        return x, y, state


class AlienBasic(Main):
    def AlienBasicMovement(self, x, y, x_del, y_del):
        global bulletX, bulletY
        x += x_del
        if x <= 0:
            x_del = 3
            y += y_del
        elif x >= 736:
            x_del = -3
            y += y_del

        # Collision
        collision = Collision.isCollision(x, y, bulletX, bulletY)
        if collision:
            Collision.BulletCollison()
            x = random.randint(0, 736)
            y = random.randint(50, 150)

        return x, y, x_del, y_del


# Intial Variables
# Score
score_value = 0

# Health
health_value = 1000

# PLayer
playerX = 370
playerY = 480
playerX_del = 0
playerY_del = 0
playerIMG = pygame.image.load("images/player.png")
player = Player(playerX, playerY, playerX_del, playerY_del, playerIMG)

# bullet
bulletIMG = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bulletX_del = 0
bulletY_del = 9
bullet_state = 'ready'
bullet = Bullet(bulletX, bulletY, bulletX_del, bulletY_del, bulletIMG, bullet_state)

# basic Alien
alienbasicX = random.randint(0, 735)
alienbasicY = random.randint(50, 150)
alienbasicX_del = 5
alienbasicY_del = 40
alienbasicIMG = pygame.image.load("images/alien.png")
alienbasic = AlienBasic(alienbasicX, alienbasicY, alienbasicX_del, alienbasicY_del, alienbasicIMG)
running = True
while running:
    # R G B
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    bulletY = playerY
                    bullet_state = bullet.FireBullet(bulletX, bulletY)
            playerX_del, playerY_del = player.KeydownEvents(playerX_del, playerY_del)

        if event.type == pygame.KEYUP:
            playerX_del, playerY_del = player.KeyupEvents(playerX_del, playerY_del)

    # Player Movement
    playerX, playerY = player.PlayerMovement(playerX, playerY, playerX_del, playerY_del)

    # Bullet Movement
    bulletX, bulletY, bullet_state = bullet.BulletMovement(bulletX, bulletY, bulletY_del, bullet_state)

    # AlienBasic Movement
    alienbasicX, alienbasicY, alienbasicX_del, alienbasicY_del \
        = alienbasic.AlienBasicMovement(alienbasicX, alienbasicY, alienbasicX_del,alienbasicY_del)

    # PlayerCollision with Basic Alien
    Collision.PlayerCollsion(playerX, playerY, alienbasicX, alienbasicY)

    # displaying objects
    player.Display(playerX, playerY, playerIMG)
    alienbasic.Display(alienbasicX, alienbasicY, alienbasicIMG)

    # GUI update
    pygame.time.Clock()
    pygame.display.update()
