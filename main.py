import pygame
from node import Node

display = pygame.display.set_mode( (800, 600) )

nodes = [Node('1', 50, 50), Node('2', 100, 200), Node('3', 400, 500)]

clock = pygame.time.Clock()
while 1:
    display.fill(pygame.Color('grey'))
    for n in nodes:
        n.draw(display)
    pygame.display.update()

    clock.tick(60)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            raise SystemExit

