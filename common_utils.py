import pygame
from data import Data
import math

def det(a,b,c,d,e,f,g,h,i):
    return a*e*i + b*f*g + c*d*h - a*f*h - b*d*i - c*e*g

def circleFromThreePoints(x1, y1, x2, y2, x3, y3):
    a = det(x1, y1, 1, x2, y2, 1, x3, y3, 1)
    bx = -det(x1*x1 + y1*y1, y1, 1, x2*x2 + y2*y2, y2, 1, x3*x3 + y3*y3, y3, 1)
    by = det(x1*x1 + y1*y1, x1, 1, x2*x2 + y2*y2, x2, 1, x3*x3 + y3*y3, x3, 1)
    c = -det(x1*x1 + y1*y1, x1, y1, x2*x2 + y2*y2, x2, y2, x3*x3 + y3*y3, x3, y3)
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

def draw_text(surface, original_text, x, y, angle=None, selected=False):
    print('TODO: draw_text not implemented')

