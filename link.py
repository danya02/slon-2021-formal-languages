import pygame
import node
import math

class Link:
    def __init__(self, node1, node2, control_point=None,
                 color='black', width=2):
        self.node1 = node1
        self.node2 = node2
        self.control_point = control_point
        self.width = width
        self.color = pygame.Color(color)

    def draw(self, surface):
        if self.control_point is None:
            pygame.draw.line(surface, self.color, (self.node1.x, self.node1.y), (self.node2.x, self.node2.y), self.width)
            self.draw_arrowhead(surface, math.atan2(self.node2.y - self.node1.y, self.node2.x - self.node1.x))

        else:
            # algorithm for finding circle taken from https://stackoverflow.com/a/28910804/5936187
            x = self.node1.x + self.node1.y * 1j
            y = self.node2.x + self.node2.y * 1j
            z = self.control_point[0] + self.control_point[1]*1j
            w = z - x
            w /= y - x
            c = (x - y) * (w - abs(w)**2) / 2j / w.imag - x
            c = -c

            v1 = (x - c)
            v2 = (y - c)

            diff = math.acos( (v1.real*v2.real + v1.imag*v2.imag) / (abs(v1)*abs(v2)) )
            ang = math.atan2( v2.imag, v2.real )
            rect = pygame.Rect(0, 0, int(abs(c-x)*2), int(abs(c-x)*2))
            rect.center = ( int(c.real), int(c.imag) )
            pygame.draw.arc(surface, self.color, rect, -ang, diff-ang, 1)
            self.draw_arrowhead(surface, diff-ang)


    def draw_arrowhead(self, surface, angle):
        x = self.node2.x
        y = self.node2.y
        dx = math.cos(angle)
        dy = math.sin(angle)
        polygon = [(x, y), (x - 8 * dx + 5 * dy, y - 8 * dy - 5 * dx), (x - 8 * dx - 5 * dy, y - 8 * dy + 5 * dx)]
        polygon = [(int(x), int(y)) for x, y in polygon]
        pygame.draw.polygon(surface, self.color, polygon)
