import pygame


def scale(image, scale):
    size = image.get_size()
    size = list(size)
    size[0] = size[0] * scale
    size[1] = size[1] * scale
    size = tuple(size)
    return pygame.transform.scale(image, size)


front = scale(pygame.image.load('assets/char_front.png'), 3)
bottom = scale(pygame.image.load('assets/char_bottom.png'), 3)
right = scale(pygame.image.load('assets/char_right.png'), 3)
left = scale(pygame.image.load('assets/char_left.png'), 3)


def moves(p1, p2, keys):
    horizontal = False
    if keys[pygame.K_z]:
        p1.move("front")
        horizontal = True
    if keys[pygame.K_s]:
        p1.move("bottom")
        horizontal = True
    if not horizontal:
        if keys[pygame.K_d]:
            p1.move("right")
        if keys[pygame.K_q]:
            p1.move("left")

    horizontal = False
    if keys[pygame.K_UP]:
        p2.move("front")
        horizontal = True
    if keys[pygame.K_DOWN]:
        p2.move("bottom")
        horizontal = True
    if not horizontal:
        if keys[pygame.K_RIGHT]:
            p2.move("right")
        if keys[pygame.K_LEFT]:
            p2.move("left")

    if p1.x > 1600:
        p1.x = 0
    elif p1.x < 0:
        p1.x = 1600
    if p2.x > 1600:
        p2.x = 0
    elif p2.x < 0:
        p2.x = 1600

    if p1.y < 0:
        p1.y = 800
    elif p1.y > 800:
        p1.y = 0
    if p2.y < 0:
        p2.y = 800
    elif p2.y > 800:
        p2.y = 0


class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.hp = 3
        self.cSprite = front

    def move(self, o):
        if o == "left":
            self.x = self.x - self.speed
            self.cSprite = left
        elif o == "right":
            self.x = self.x + self.speed
            self.cSprite = right
        elif o == "bottom":
            self.y = self.y + self.speed
            self.cSprite = bottom
        else:
            self.y = self.y - self.speed
            self.cSprite = front

    def sprite(self):
        return self.cSprite

    def coords(self):
        return (self.x, self.y)

    def rect(self):
        if self.cSprite == front or self.cSprite == bottom:
            return pygame.Rect((self.x, self.y), (54, 72))
        return pygame.Rect((self.x, self.y), (72, 54))

    def nRect(self, o):
        if o == "front":
            return pygame.Rect((self.x, self.y - self.speed), (54, 72))
        if o == "bottom":
            return pygame.Rect((self.x, self.y + self.speed), (54, 72))
        if o == "right":
            return pygame.Rect((self.x + self.speed, self.y), (72, 54))
        return pygame.Rect((self.x - self.speed, self.y), (72, 54))
