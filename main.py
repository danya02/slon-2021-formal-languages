import pygame

display = pygame.display.set_mode( (800, 600) )


while 1:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            raise SystemExit

