import pygame
import math
import random
from classes import *


# event class
class EventChange():
    @staticmethod
    def KeydownEvents(x_del, y_del):

        if event.key == pygame.K_LEFT:
            x_del = -7
        if event.key == pygame.K_RIGHT:
            x_del = 7
        if event.key == pygame.K_UP:
            y_del = -7
        if event.key == pygame.K_DOWN:
            y_del = 7

        return x_del, y_del

    @staticmethod
    def KeyupEvents(x_del, y_del):

        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            x_del = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            y_del = 0

        return x_del, y_del


# initalise the pygame
pygame.init()

# create the screen (W, H)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Title and Icon (32pxlby32pxl)
pygame.display.set_caption("Starkiller")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Intial Variables

# difficulty
score_value = 0
basicaliendiff = 3
asteroiddiff = 10

# Health
health_value = 1000

# PLayer
player = Creating.PlayerCreate()

# bullet
bullet = Creating.BulletCreate()

# basic Alien
alienbasic = []
alienbasic.append(Creating.BasicAlienCreate())

# asteroid
asteroid = []


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
            player.x_del, player.y_del = EventChange.KeydownEvents(player.x_del, player.y_del)

        if event.type == pygame.KEYUP:
            player.x_del, player.y_del = EventChange.KeyupEvents(player.x_del, player.y_del)

    # Player Movement
    player.PlayerMovement()

    # Bullet Movement
    bullet.BulletMovement()

    # basic alien stuff
    for i in alienbasic:
        # AlienBasic Movement
        i.AlienBasicMovement()

        # Player Collision with Basic Alien
        health_value, running = player.PlayerCollsion(i.x, i.y, health_value, running)

        # Basic Alien Collison with Bullet
        hit = i.BasicAlienBulletCollision(bullet.x, bullet.y)
        if hit == "Yes":
            bullet.state = 'ready'
            score_value += 1
            print(score_value)
            basicaliendiff, asteroiddiff, alienbasic, asteroid = Difficulty.IncreasingDifficulty(score_value, alienbasic, asteroid, basicaliendiff, asteroiddiff)

        # displaying BasicAlienObject
        i.Display()

    # asteroid stuff
    for i in asteroid:
        # Asteroid Movement
        i.AsteroidMovement()

        # Player Collision with Basic Alien
        health_value, running = player.PlayerCollsion(i.x, i.y, health_value, running)

        i.Display()

    # displaying Player objects
    player.Display()

    # GUI update
    pygame.time.Clock()
    pygame.display.update()
