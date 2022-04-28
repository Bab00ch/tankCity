import random
import pygame
from random import randint


def scale(image, scale):
    size = image.get_size()
    size = list(size)
    size[0] = size[0] * scale
    size[1] = size[1] * scale
    size = tuple(size)
    return pygame.transform.scale(image, size)


up = scale(pygame.image.load('assets/tank_up.png'), 2)
down = scale(pygame.image.load('assets/tank_down.png'), 2)
right = scale(pygame.image.load('assets/tank_right.png'), 2)
left = scale(pygame.image.load('assets/tank_left.png'), 2)
brick = scale(pygame.image.load('assets/brick.png'), 2)
bullet_left = scale(pygame.image.load('assets/bullet_0.png'), 2)
bullet_down = scale(pygame.image.load('assets/bullet_1.png'), 2)
bullet_right = scale(pygame.image.load('assets/bullet_2.png'), 2)
bullet_up = scale(pygame.image.load('assets/bullet_3.png'), 2)
teleport = pygame.image.load('assets/teleport.png')
heart = pygame.image.load('assets/heart.png')
bullet_pow = pygame.image.load("assets/bullet_gui.png")
horizontal = False


def moves(p1, p2, keys, bricks):
    global horizontal
    if keys[pygame.K_z]:
        p1.move("up", bricks)
        horizontal = True
    if keys[pygame.K_s]:
        p1.move("down", bricks)
        horizontal = True
    if not horizontal:
        if keys[pygame.K_d]:
            p1.move("right", bricks)
        if keys[pygame.K_q]:
            p1.move("left", bricks)
    horizontal = False
    if keys[pygame.K_UP]:
        p2.move("up", bricks)
        horizontal = True
    if keys[pygame.K_DOWN]:
        p2.move("down", bricks)
        horizontal = True
    if not horizontal:
        if keys[pygame.K_RIGHT]:
            p2.move("right", bricks)
        if keys[pygame.K_LEFT]:
            p2.move("left", bricks)

    if p1.x > 576:
        p1.x = 576
    elif p1.x < 0:
        p1.x = 0

    if p2.x > 576:
        p2.x = 576
    elif p2.x < 0:
        p2.x = 0

    if p1.y > 576:
        p1.y = 576
    elif p1.y < 0:
        p1.y = 0

    if p2.y > 576:
        p2.y = 576
    elif p2.y < 0:
        p2.y = 0


class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tpx = 0
        self.tpy = 0
        self.speed = 3
        self.hp = 3
        self.cSprite = up
        self.bullets = 3
        self.bullet_count = 0
        self.maxBullets = 3
        self.teleports = 0
        self.teleporting = False

    def move(self, o, bricks):
        if o == "left":
            for i in bricks:
                if self.nRect("left").colliderect(i.rect()):
                    self.cSprite = left
                    return
            self.x = self.x - self.speed
            self.cSprite = left
        elif o == "right":
            for i in bricks:
                if self.nRect("right").colliderect(i.rect()):
                    self.cSprite = right
                    return
            self.x = self.x + self.speed
            self.cSprite = right
        elif o == "down":
            for i in bricks:
                if self.nRect("down").colliderect(i.rect()):
                    self.cSprite = down
                    return
            self.y = self.y + self.speed
            self.cSprite = down
        else:
            for i in bricks:
                if self.nRect("up").colliderect(i.rect()):
                    self.cSprite = up
                    return
            self.y = self.y - self.speed
            self.cSprite = up

    def orientation(self):
        if self.cSprite == up:
            return "up"
        elif self.cSprite == down:
            return "down"
        elif self.cSprite == right:
            return "right"
        return "left"

    def sprite(self):
        return self.cSprite

    def coords(self):
        return (self.x, self.y)

    def rect(self):
        return pygame.Rect((self.x + 8, self.y + 8), (48, 48))

    def tpRect(self):
        return pygame.Rect((self.tpx + 8, self.tpy + 8), (48, 48))

    def nRect(self, o):
        if o == "up":
            return pygame.Rect((self.x + 8, self.y + 8 - self.speed), (48, 48))
        if o == "down":
            return pygame.Rect((self.x + 8, self.y + 8 + self.speed), (48, 48))
        if o == "right":
            return pygame.Rect((self.x + 8 + self.speed, self.y + 8), (48, 48))
        return pygame.Rect((self.x + 8 - self.speed, self.y + 8), (48, 48))

    def frame(self):
        if self.bullets < self.maxBullets:
            self.bullet_count = self.bullet_count + 1
            if self.bullet_count > 180:
                self.bullets = self.bullets + 1
                self.bullet_count = 0
        if not self.teleporting:
            if self.cSprite == teleport:
                self.cSprite = up

    def canShoot(self):
        if not self.bullets == 0:
            self.bullets = self.bullets - 1
            return True
        return False

    def getBullets(self):
        return self.bullets

    def getHP(self):
        return self.hp

    def getPowerUp(self, powerUp, brickList):
        if powerUp.getType() == "heart" and self.hp < 5:
            self.hp = self.hp + 1
        elif powerUp.getType() == "bullet" and self.maxBullets < 5:
            self.maxBullets = self.maxBullets + 1
        elif powerUp.getType() == "teleporter" and self.teleports < 1:
            self.teleports = 1
            while True:
                collide = False
                self.tpx = randint(0, 576)
                self.tpy = randint(0, 576)
                for i in brickList:
                    if self.tpRect().colliderect(i.rect()):
                        collide = True
                if not collide:
                    break

    def doTeleport(self):
        self.x = self.tpx
        self.y = self.tpy
        self.teleports = 0

    def tpCoords(self):
        return (self.tpx, self.tpy)

    def tpSprite(self):
        return teleport

    def haveKilled(self,brickList):
        while True:
            collide = False
            self.x = randint(0, 576)
            self.y = randint(0, 576)
            for i in brickList:
                if self.rect().colliderect(i.rect()):
                    collide = True
            if not collide:
                break


class newBrick:
    def __init__(self, x, y):
        self.x = x * 64
        self.y = y * 64
        self.cSprite = brick

    def sprite(self):
        return self.cSprite

    def rect(self):
        return pygame.Rect((self.x, self.y), (64, 64))

    def coords(self):
        return (self.x, self.y)


class newBullet:
    def __init__(self, x, y, o, sender):
        self.x = x
        self.y = y
        self.speed = 8
        self.o = o
        self.sender = sender
        if self.o == "up":
            self.cSprite = bullet_up
        elif self.o == "down":
            self.cSprite = bullet_down
        elif self.o == "right":
            self.cSprite = bullet_right
        else:
            self.cSprite = bullet_left

    def sprite(self):
        return self.cSprite

    def rect(self):
        return pygame.Rect((self.x, self.y), (16, 16))

    def coords(self, players, bricks):
        if self.o == "right":
            self.x = self.x + self.speed
        elif self.o == "left":
            self.x = self.x - self.speed
        elif self.o == "up":
            self.y = self.y - self.speed
        else:
            self.y = self.y + self.speed

        return (self.x, self.y)


class powerUp:
    def __init__(self, x, y, ):
        powerUpsList = ["heart", "bullet", "teleporter"]
        self.x = x + randint(16, 48)
        self.y = y + randint(16, 48)
        self.type = powerUpsList[randint(0,len(powerUpsList)-1)]

    def render(self):
        if self.type == "heart":
            return heart
        elif self.type == "bullet":
            return bullet_pow
        elif self.type == "teleporter":
            return teleport

    def coords(self):
        return (self.x, self.y)

    def rect(self):
        return pygame.Rect((self.x, self.y), (16, 16))

    def getType(self):
        return self.type