import pygame
from data import Data
import math
import config

def det(a,b,c,d,e,f,g,h,i):
    return a*e*i + b*f*g + c*d*h - a*f*h - b*d*i - c*e*g

def circle_from_three_points(x1, y1, x2, y2, x3, y3):
    a = det(x1, y1, 1, x2, y2, 1, x3, y3, 1)
    bx = -det(x1*x1 + y1*y1, y1, 1, x2*x2 + y2*y2, y2, 1, x3*x3 + y3*y3, y3, 1)
    by = det(x1*x1 + y1*y1, x1, 1, x2*x2 + y2*y2, x2, 1, x3*x3 + y3*y3, x3, 1)
    c = -det(x1*x1 + y1*y1, x1, y1, x2*x2 + y2*y2, x2, y2, x3*x3 + y3*y3, x3, y3)
    if a == 0: a = 0.1
    return Data(
        x = -bx / (2*a),
        y = -by / (2*a),
        radius = math.sqrt(bx*bx + by*by - 4*a*c) / (2 * abs(a))
    )

def draw_arrow(surface, x, y, angle):
    dx = math.cos(angle)
    dy = math.sin(angle)
    polygon = [ (x, y), (x - 8 * dx + 5 * dy, y - 8 * dy - 5 * dx), (x - 8 * dx - 5 * dy, y - 8 * dy + 5 * dx) ]
    pygame.draw.polygon(surface, pygame.Color('black'), polygon)

font = None

def draw_text(surface, original_text, x, y, angle=None, selected=False):
    global font
    if font is None:
        font = pygame.font.get_fonts()[0]
        font = pygame.font.SysFont(font, 20)
    surf = font.render(original_text, True, pygame.Color('black'))
    r = surf.get_rect()
    r.x = x
    r.y = y
    r.x -= r.width // 2
    if angle is not None:
        cos = math.cos(angle)
        sin = math.sin(angle)
        cpx = (r.width/2 + 5) * (int(cos>0) * 2 - 1)
        cpy = (r.height/2 + 5) * (int(sin>0) * 2 - 1)
        slide = sin * (abs(sin) ** 40) * cpx - cos * (abs(cos)**10) * cpy
        r.x += cpx - sin * slide
        r.y += cpy + cos * slide
    surface.blit(surf, r)

def snap_node(node, nodes):
    for i in nodes:
        if i is node: continue
        if abs(node.x - i.x) < config.snap_to_padding: node.x = i.x
        if abs(node.y - i.y) < config.snap_to_padding: node.y = i.y

def select_object(x, y, *object_lists):
    for l in object_lists:
        for obj in l:
            if obj.contains_point(x, y):
                return obj
    return None

