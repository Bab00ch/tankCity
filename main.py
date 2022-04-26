import pygame
from random import randint

import lib

pygame.init()
surface = pygame.display.set_mode((640,704))
pygame.display.set_caption("Battle City")
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
pygame.mixer.music.load("assets/city.mp3")
pygame.mixer.music.play(-1)
laser=pygame.mixer.Sound("assets/hit.mp3")
explosion=pygame.mixer.Sound("assets/explosion.mp3")
player1_img = pygame.image.load('assets/player1.png')
player2_img = pygame.image.load('assets/player2.png')
won = pygame.image.load('assets/won.png')
bullets_img = lib.scale(pygame.image.load('assets/bullets.png'),0.5)
background = lib.scale(pygame.image.load('assets/background.png'),4)
bullet_gui = lib.scale(pygame.image.load('assets/bullet_gui.png'),2)
heart = lib.scale(pygame.image.load('assets/heart.png'),2)
teleport_gui = lib.scale(pygame.image.load('assets/teleport.png'),2)


clock = pygame.time.Clock()

bricks = []
for i in range(0,10):
    bricks.append(lib.newBrick(2, i))
    bricks.append(lib.newBrick(7, i))
for i in range(0,10):
    bricks.append(lib.newBrick(i, 2))
    bricks.append(lib.newBrick(i, 7))

x = 0
for i in bricks:
    for j in bricks:
        if not i == j:
            if i.coords() == j.coords():
                del bricks[x]
    x = x + 1

powerUps = []
p1 = lib.player(0, 0)
p2 = lib.player(576, 576)
players = [p1,p2]
bullets = []
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if p1.canShoot():
                    bullets.append(lib.newBullet(p1.x + 16, p1.y + 16, p1.orientation(), p1))
                    laser.play()
            if event.key == pygame.K_m:
                if p2.canShoot():
                    bullets.append(lib.newBullet(p2.x + 16, p2.y + 16, p2.orientation(), p2))
                    laser.play()
            if event.key == pygame.K_e:
                if p1.teleports == 1:
                    p1.doTeleport(bricks)
            if event.key == pygame.K_l:
                if p2.teleports == 1:
                    p2.doTeleport(bricks)
    keys = pygame.key.get_pressed()
    lib.moves(p1,p2,keys,bricks)
    for d in range(0,10):
        for f in range(0, 10):
            surface.blit(background,(d*64,f*64))
    surface.blit(p1.sprite(), p1.coords())
    surface.blit(p2.sprite(), p2.coords())
    for i in bricks:
        surface.blit(i.sprite(), i.coords())
    for i in bullets:
        bullet = i
        for b in bricks:
            if i.rect().colliderect(b.rect()):
                bullets.remove(i)
                bricks.remove(b)
                if randint(0,5) == 3:
                    powerUps.append(lib.powerUp(b.x,b.y))
                break
        for p in players:
            if i.rect().colliderect(p.rect()):
                if not p == i.sender:
                    bullets.remove(i)
                    p.hp = p.hp - 1
                    print(p.hp)
                    explosion.play()
                    if p.hp == 0:
                        running = False
                        loser = p
                    break
    for p in players:
        p.frame()
    for p in powerUps:
        for i in players:
            if p.rect().colliderect(i.rect()):
                i.getPowerUp(p)
                powerUps.remove(p)
        else:
            surface.blit(p.render(), p.coords())
    for i in bullets:
        surface.blit(i.sprite(), i.coords(players, bricks))
    pygame.draw.rect(surface, (128, 128, 128), pygame.Rect(0, 640, 640, 64))
    for i in range(0,p1.getBullets()):
        surface.blit(bullet_gui,(i*32,640))
    for i in range(0,p2.getBullets()):
        a = i*32
        a = a + 32
        surface.blit(bullet_gui, (640-a, 640))

    for i in range(0,p1.getHP()):
        surface.blit(heart,(i*32,672))
    if p1.teleports == 1:
        surface.blit(teleport_gui, (i * 32 + 32, 640))
    for i in range(0,p2.getHP()):
        a = i*32
        a = a + 32
        surface.blit(heart, (640-a, 672))
    if p2.teleports == 1:
        surface.blit(teleport_gui, (576-a, 640))

    pygame.display.flip()
    clock.tick(120)
x = 250
y = 100
a = 0

for i in range(0, 60):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    surface.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(120)

for i in range(0,60):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    surface.fill((0, 0, 0))
    if p2 == loser:
        surface.blit(player1_img, (x,y))
    else:
        surface.blit(player2_img, (x, y))
    pygame.display.flip()
    clock.tick(120)
explosion.play()
pygame.time.wait(500)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    surface.fill((0, 0, 0))
    if p2 == loser:
        surface.blit(player1_img, (x,y))
    else:
        surface.blit(player2_img, (x, y))
    surface.blit(won, (400, 400))
    pygame.display.flip()
    clock.tick(120)