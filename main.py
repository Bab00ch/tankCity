import pygame
import lib

pygame.init()
surface = pygame.display.set_mode((640,640))
pygame.display.set_caption("Battle City")
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

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
bullets = [lib.newBullet(250, 250,"up",p1)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(lib.newBullet(p1.x + 16, p1.y + 16, p1.orientation(), p1))
    keys = pygame.key.get_pressed()
    lib.moves(p1,p2,keys,bricks)
    pygame.draw.rect(surface, (0,0,0), pygame.Rect((0, 0), (960, 960)))
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
                    break

    pygame.display.flip()
    clock.tick(120)