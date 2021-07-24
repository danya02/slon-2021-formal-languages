import pygame
from node import Node
from link import Link
import random

display = pygame.display.set_mode( (800, 600) )

nodes = [Node('1', 50, 50), Node('2', 100, 200), Node('3', 400, 500)]
links = [Link(nodes[0], nodes[1]), Link(nodes[1], nodes[2], (300, 300))]
clock = pygame.time.Clock()
while 1:
    display.fill(pygame.Color('grey'))
    for n in nodes:
        n.draw(display)
    for l in links:
        l.draw(display)
    pygame.display.update()
    nodes[2].x += random.randint(0, 2) - 1
    nodes[2].y += random.randint(0, 2) - 1

    clock.tick(60)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            raise SystemExit

