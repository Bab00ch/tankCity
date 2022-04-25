import pygame
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
p1_bullets = 100
p2_bullets = 100


clock = pygame.time.Clock()

bricks = []
for i in range(0,10):
    bricks.append(lib.newBrick(2, i))
    bricks.append(lib.newBrick(7, i))
for i in range(0,10):
    bricks.append(lib.newBrick(i, 2))
    bricks.append(lib.newBrick(i, 7))
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
                if p1_bullets > 25:
                    bullets.append(lib.newBullet(p1.x + 16, p1.y + 16, p1.orientation(), p1))
                    laser.play()
                    p1_bullets -= 25
            if event.key == pygame.K_m:
                if p2_bullets > 25:
                    bullets.append(lib.newBullet(p2.x + 16, p2.y + 16, p2.orientation(), p2))
                    laser.play()
                    p2_bullets -= 25
    if p1_bullets < 100:
        p1_bullets = p1_bullets + 0.25
    if p2_bullets < 100:
        p2_bullets = p2_bullets + 0.25
    keys = pygame.key.get_pressed()
    lib.moves(p1,p2,keys,bricks)
    pygame.draw.rect(surface, (0,0,0), pygame.Rect((0, 0), (960, 960)))
    pygame.draw.rect(surface, (0, 0, 255), pygame.Rect((0, 684), (p1_bullets, 20)))
    pygame.draw.rect(surface, (0, 0, 255), pygame.Rect((640-p2_bullets, 684), (100, 20)))
    surface.blit(p1.sprite(), p1.coords())
    surface.blit(p2.sprite(), p2.coords())
    for i in bricks:
        surface.blit(i.sprite(), i.coords())
    for i in bullets:
        surface.blit(i.sprite(), i.coords(players,bricks))
    for i in bullets:
        bullet = i
        for b in bricks:
            if i.rect().colliderect(b.rect()):
                bullets.remove(i)
                bricks.remove(b)
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
    surface.blit(bullets_img,(0,640))
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