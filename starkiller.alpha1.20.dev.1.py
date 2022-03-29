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

class Creating:
    @staticmethod
    def BasicAlienCreate(alien, num):
        for i in range(0, num + 1):
            alienbasicX = random.randint(0, 735)
            alienbasicY = random.randint(50, 150)
            alienbasicX_del = 5
            alienbasicY_del = 40
            alienbasicIMG = pygame.image.load("images/alien.png")
            alien.append(AlienBasic(alienbasicX, alienbasicY, alienbasicX_del, alienbasicY_del, alienbasicIMG))
        return alien

    @staticmethod
    def PlayerCreate():
        playerX = 370
        playerY = 480
        playerX_del = 0
        playerY_del = 0
        playerIMG = pygame.image.load("images/player.png")
        return Player(playerX, playerY, playerX_del, playerY_del, playerIMG)

    @staticmethod
    def BulletCreate():
        bulletIMG = pygame.image.load("images/bullet.png")
        bulletX = 0
        bulletY = 480
        bulletX_del = 0
        bulletY_del = 9
        bullet_state = 'ready'
        return Bullet(bulletX, bulletY, bulletX_del, bulletY_del, bulletIMG, bullet_state)


# MAIN Class
class Main:
    def __init__(self, x, y, x_del, y_del, img):
        self.x = x
        self.y = y
        self.x_del = x_del
        self.y_del = y_del
        self.img = img

    def Display(self):
        screen.blit(self.img, (self.x, self.y))

    def KeydownEvents(self):

        if event.key == pygame.K_LEFT:
            self.x_del = -7
        if event.key == pygame.K_RIGHT:
            self.x_del = 7
        if event.key == pygame.K_UP:
            self.y_del = -7
        if event.key == pygame.K_DOWN:
            self.y_del = 7

    def KeyupEvents(self):
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            self.x_del = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            self.y_del = 0


# PLayer Class
class Player(Main):
    def PlayerMovement(self):
        self.x += self.x_del
        self.y += self.y_del
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736
        if self.y <= 0:
            self.y = 0
        elif self.y >= 536:
            self.y = 536

    def PlayerCollsion(self, x2, y2):
        global health_value, running
        isCollision = Collision.isCollision(self.x, self.y, x2, y2)
        if isCollision:
            health_value -= 10
            print(health_value)
            if health_value == 0:
                running = False


# Bullet Class
class Bullet(Main):
    def __init__(self, x, y, x_del, y_del, img, state):
        super().__init__(x, y, x_del, y_del, img)
        self.state = state

    def FireBullet(self):
        self.state = "fire"
        screen.blit(self.img, (self.x + 16, self.y + 10))
        return self.state

    def BulletMovement(self):
        if self.y <= 0:
            self.y = 480
            self.state = 'ready'
        if self.state == 'fire':
            self.state = self.FireBullet()
            self.y -= self.y_del


class AlienBasic(Main):
    def AlienBasicMovement(self):
        self.x += self.x_del
        if self.x <= 0:
            self.x_del = 3
            self.y += self.y_del
        elif self.x >= 736:
            self.x_del = -3
            self.y += self.y_del

    def BasicAlienBulletCollision(self, x2, y2):
        isCollision = Collision.isCollision(self.x, self.y, x2, y2)
        if isCollision:
            self.x = random.randint(0, 736)
            self.y = random.randint(50, 150)
            return "Yes"

# Intial Variables
# Score
score_value = 0

# Health
health_value = 1000

# PLayer
player = Creating.PlayerCreate()

# bullet
bullet = Creating.BulletCreate()

# basic Alien
alienbasic = []
num_basic_aliens = 2
Creating.BasicAlienCreate(alienbasic, num_basic_aliens)

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
                if bullet.state == 'ready':
                    bullet.x = player.x
                    bullet.y = player.y
                    bullet.state = bullet.FireBullet()
            player.KeydownEvents()

        if event.type == pygame.KEYUP:
            player.KeyupEvents()

    # Player Movement
    player.PlayerMovement()

    # Bullet Movement
    bullet.BulletMovement()

    for i in alienbasic:
        # AlienBasic Movement
        i.AlienBasicMovement()

        # Player Collision with Basic Alien
        player.PlayerCollsion(i.x, i.y)

        # Basic Alien Collison with Bullet
        hit = i.BasicAlienBulletCollision(bullet.x, bullet.y)
        if hit == "Yes":
            bullet.state = 'ready'
            score_value += 1
            print(score_value)

        # displaying BasicAlienObject
        i.Display()

    # displaying Player objects
    player.Display()

    # GUI update
    pygame.time.Clock()
    pygame.display.update()
