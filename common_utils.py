import pygame
from data import Data
import math
import config
import hashlib
import random
import colorlib

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

def draw_arrow(surface, x, y, angle, color=pygame.Color('black')):
    dx = math.cos(angle)
    dy = math.sin(angle)
    polygon = [ (x, y), (x - 8 * dx + 5 * dy, y - 8 * dy - 5 * dx), (x - 8 * dx - 5 * dy, y - 8 * dy + 5 * dx) ]
    pygame.draw.polygon(surface, color, polygon)

font = None

def draw_text(surface, original_text, x, y, angle=None, color=pygame.Color('black'), caret_visible=None):
    global font
    if font is None:
        font = pygame.font.SysFont('Arial', 20)
    surf = font.render(original_text, True, color)
    r = surf.get_rect()
    r.centerx = x
    r.centery = y
    #r.x -= r.width // 2
    if angle is not None:
        cos = math.cos(angle)
        sin = math.sin(angle)
        cpx = (r.width/2 + 5) * (int(cos>0) * 2 - 1)
        cpy = (r.height/2 + 5) * (int(sin>0) * 2 - 1)
        slide = sin * (abs(sin) ** 40) * cpx - cos * (abs(cos)**10) * cpy
        r.x += cpx - sin * slide
        r.y += cpy + cos * slide
    surface.blit(surf, r)
    if caret_visible:
        pygame.draw.line(surface, color, (r.right, r.bottom), (r.right, r.top), 3)


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

def color_from_hash(name):
    name = bytes(name, 'utf8')
    h = hashlib.md5(name).hexdigest()
    hi = int(h, 16)
    random.seed(hi)
    hue = random.random()
    saturation = random.random()
    saturation = (saturation/2) + 0.5
    r,g,b = colorlib.hsv_to_rgb(hue, saturation, 1)
    r,g,b = map(lambda x: int(x*255), (r,g,b))
    return pygame.Color(r,g,b)


def get_color(self, selected, node_cursors=[], link_cursors=[], **kwargs):
    cursors = [i[0] for i in node_cursors+link_cursors]
    # TODO: use color_from_hash to color nodes and links
    if self is selected: return pygame.Color('blue')
    return pygame.Color('black')
