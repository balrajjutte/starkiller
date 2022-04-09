import pygame
import math
import random

# create the screen (W, H)
screen = pygame.display.set_mode((800, 600))


# difficulty
class Difficulty():
    @staticmethod
    def IncreasingDifficulty(score, aliens, asteroid, aliendiff, asteroiddiff):
        if score == aliendiff and score < 100:
            aliendiff += 5
            aliens.append(Creating.BasicAlienCreate())

        if score == asteroiddiff and score < 100:
            asteroiddiff += 30
            asteroid.append(Creating.AsteroidCreate())

        return aliendiff, asteroiddiff, aliens, asteroid


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
    def BasicAlienCreate():
        alienbasicX = random.randint(0, 735)
        alienbasicY = random.randint(50, 150)
        alienbasicX_del = 5
        alienbasicY_del = 40
        alienbasicIMG = pygame.image.load("alien.png")
        return AlienBasic(alienbasicX, alienbasicY, alienbasicX_del, alienbasicY_del, alienbasicIMG)

    @staticmethod
    def PlayerCreate():
        playerX = 370
        playerY = 480
        playerX_del = 0
        playerY_del = 0
        playerIMG = pygame.image.load("player.png")
        return Player(playerX, playerY, playerX_del, playerY_del, playerIMG)

    @staticmethod
    def BulletCreate():
        bulletIMG = pygame.image.load("bullet.png")
        bulletX = 0
        bulletY = 480
        bulletX_del = 0
        bulletY_del = 9
        bullet_state = 'ready'
        return Bullet(bulletX, bulletY, bulletX_del, bulletY_del, bulletIMG, bullet_state)

    @staticmethod
    def AsteroidCreate():
        asteroidX = random.randint(40, 700)
        asteroidY = 0
        asteroidX_del = 0
        asteroidY_del = random.randint(1,7)
        asteroidIMG = pygame.image.load("asteroid.png")
        return Asteroid(asteroidX, asteroidY, asteroidX_del, asteroidY_del, asteroidIMG)


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

    def PlayerCollsion(self, x2, y2, health_value, running):
        isCollision = Collision.isCollision(self.x, self.y, x2, y2)
        if isCollision:
            health_value -= 10
            print(health_value)
            if health_value == 0:
                running = False

        return health_value, running


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
        if self.y >= 536:
            self.x = random.randint(0, 736)
            self.y = random.randint(0, 100)

    def BasicAlienBulletCollision(self, x2, y2):
        isCollision = Collision.isCollision(self.x, self.y, x2, y2)
        if isCollision:
            self.x = random.randint(0, 736)
            self.y = random.randint(0, 100)
            return "Yes"


class Asteroid(Main):
    def AsteroidMovement(self):
        self.y += self.y_del
        if self.y >= 536:
            self.y = random.randint(-1600, 0)
            self.x = random.randint(40, 700)
            self.y_del = random.randint(3,7)
