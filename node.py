import pygame

class Node:
    def __init__(self, name, x, y, radius=20,
                fill_color='white', stroke_color='black',
                stroke_width=2):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.fill_color = pygame.Color(fill_color)
        self.stroke_color = pygame.Color(stroke_color)
        self.stroke_width = stroke_width

    def draw(self, surface):
        pygame.draw.circle(surface, self.fill_color, (self.x, self.y), self.radius)
        if self.stroke_width:
            pygame.draw.circle(surface, self.stroke_color, (self.x, self.y), self.radius, width=self.stroke_width)
