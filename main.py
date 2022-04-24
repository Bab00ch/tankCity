import pygame
import lib

pygame.init()
surface = pygame.display.set_mode((1600,800))
pygame.display.set_caption("Battle City")
pygame.display.set_icon(pygame.image.load('assets/icon.png'))

clock = pygame.time.Clock()

p1 = lib.player(400, 400)
p2 = lib.player(1200, 400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    keys = pygame.key.get_pressed()
    lib.moves(p1,p2,keys)
    pygame.draw.rect(surface, (0,0,0), pygame.Rect((0, 0), (1600, 800)))
    pygame.draw.rect(surface, (255,0,0), p1.rect())
    surface.blit(p1.sprite(),p1.coords())
    pygame.draw.rect(surface, (255, 0, 0), p2.rect())
    surface.blit(p2.sprite(), p2.coords())
    pygame.display.flip()
    clock.tick(120)