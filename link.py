import pygame
import math
from data import Data
import config
import common_utils
import random

class Link:
    def __init__(self, a, b):
        self.nodeA = a
        self.nodeB = b
        self.text = ''
        self.line_angle_adjust = 0  # value to add to text_angle when link is straight line
        
        # make anchor point relative to the locations of nodeA and nodeB
        self.parallel_part = 0.5  # percentage from nodeA to nodeB
        self.perpendicular_part = 0  # pixels from line between nodeA and nodeB

    def get_anchor_point(self):
        dx = self.nodeB.x - self.nodeA.x
        dy = self.nodeB.y - self.nodeA.y
        scale = math.sqrt(dx*dx + dy*dy)
        try:
            return Data(
                x = self.nodeA.x + dx * self.parallel_part - dy * self.perpendicular_part / scale,
                y = self.nodeA.y + dy * self.parallel_part + dx * self.perpendicular_part / scale
            )
        except ZeroDivisionError:
            self.nodeA.x += random.randint(0, 30) - 15
            self.nodeA.y += random.randint(0, 30) - 15
            self.nodeB.x += random.randint(0, 30) - 15
            self.nodeB.y += random.randint(0, 30) - 15
            return Data(x=0, y=0)

    def set_anchor_point(self, x, y):
        dx = self.nodeB.x - self.nodeA.x
        dy = self.nodeB.y - self.nodeA.y
        scale = math.sqrt(dx*dx + dy*dy)
        self.parallel_part = (dx * (x - self.nodeA.x) + dy * (y - self.nodeA.y)) / (scale * scale)
        self.perpendicular_part = (dx * (y - self.nodeA.y) - dy * (x - self.nodeA.x)) / scale

        # snap to a straight line
        if self.parallel_part > 0 and self.parallel_part < 1 and abs(self.perpendicular_part) < config.snap_to_padding:
            self.line_angle_adjust = (self.perpendicular_part < 0) * math.pi
            self.perpendicular_part = 0


    def get_end_points_and_circle(self):
        if self.perpendicular_part == 0:
                midX = (self.nodeA.x + self.nodeB.x) / 2;
                midY = (self.nodeA.y + self.nodeB.y) / 2;
                start = self.nodeA.closest_point_on_circle(midX, midY);
                end = self.nodeB.closest_point_on_circle(midX, midY);
                return Data(
                    has_circle = False,
                    startX = start.x,
                    startY = start.y,
                    endX = end.x,
                    endY = end.y
                )

        anchor = self.get_anchor_point()
        circle = common_utils.circle_from_three_points(self.nodeA.x, self.nodeA.y, self.nodeB.x, self.nodeB.y, anchor.x, anchor.y)
        isReversed = (self.perpendicular_part > 0)
        reverseScale = 1 if isReversed else -1
        startAngle = math.atan2(self.nodeA.y - circle.y, self.nodeA.x - circle.x) - reverseScale * config.node_radius / circle.radius
        endAngle = math.atan2(self.nodeB.y - circle.y, self.nodeB.x - circle.x) + reverseScale * config.node_radius / circle.radius
        startX = circle.x + circle.radius * math.cos(startAngle);
        startY = circle.y + circle.radius * math.sin(startAngle);
        endX = circle.x + circle.radius * math.cos(endAngle);
        endY = circle.y + circle.radius * math.sin(endAngle);

        return Data(
            has_circle = True,
            startX = startX,
            startY = startY,
            endX = endX,
            endY = endY,
            start_angle = startAngle,
            end_angle = endAngle,
            circleX = circle.x,
            circleY = circle.y,
            circle_radius = circle.radius,
            reverse_scale = reverseScale,
            is_reversed = isReversed
        )

    def draw(self, surface, selected_object, caret_visible=None, **kwargs):
        c = common_utils.get_color(self, selected_object, **kwargs)
        stuff = self.get_end_points_and_circle()
        
        # draw arc
        if stuff.has_circle:
            r = pygame.Rect(0, 0, stuff.circle_radius*2, stuff.circle_radius*2)
            r.centerx = stuff.circleX
            r.centery = stuff.circleY
            a = self.get_anchor_point()
            sa, ea = stuff.start_angle, stuff.end_angle
            if not stuff.is_reversed: sa, ea = ea, sa
            pygame.draw.arc(surface, c, r, -sa, -ea, 3)
#            pygame.draw.circle(surface, pygame.Color('red'), (a.x, a.y), 5)
        else:
            pygame.draw.line(surface, c, (stuff.startX, stuff.startY), (stuff.endX, stuff.endY), 3 )

        # draw the head of the arrow
        if stuff.has_circle:
            common_utils.draw_arrow(surface, stuff.endX, stuff.endY, stuff.end_angle - stuff.reverse_scale * (math.pi / 2), c)
        else:
            common_utils.draw_arrow(surface, stuff.endX, stuff.endY, math.atan2(stuff.endY - stuff.startY, stuff.endX - stuff.startX), c)

        # draw the text
        if stuff.has_circle:
            startAngle = -stuff.start_angle
            endAngle = -stuff.end_angle
            if endAngle > startAngle:
                endAngle += math.pi * 2

            textAngle = (startAngle + endAngle) / 2 + stuff.is_reversed * math.pi
            textX = stuff.circleX + stuff.circle_radius * math.cos(-textAngle)
            textY = stuff.circleY + stuff.circle_radius * math.sin(-textAngle)
            common_utils.draw_text(surface, self.text, textX, textY, -textAngle, c, caret_visible)
        else:
            textX = (stuff.startX + stuff.endX) / 2
            textY = (stuff.startY + stuff.endY) / 2
            textAngle = math.atan2(stuff.endX - stuff.startX, stuff.startY - stuff.endY)
            common_utils.draw_text(surface, self.text, textX, textY, textAngle + self.line_angle_adjust, c, caret_visible)


    def contains_point(self, x, y):
        stuff = self.get_end_points_and_circle()
        if stuff.has_circle:
            dx = x - stuff.circleX
            dy = y - stuff.circleY
            distance = math.sqrt(dx*dx + dy*dy) - stuff.circle_radius
            if abs(distance) < config.hit_target_padding:
                angle = math.atan2(dy, dx)
                startAngle = stuff.start_angle
                endAngle = stuff.end_angle
                if stuff.is_reversed:
                    startAngle, endAngle = endAngle, startAngle

                if endAngle < startAngle:
                    angle += math.pi * 2
                elif angle > endAngle:
                    angle -= math.pi * 2
                
                return angle < endAngle and angle > startAngle
        else:
            dx = stuff.endX - stuff.startX
            dy = stuff.endY - stuff.startY
            length = math.sqrt(dx*dx + dy*dy)
            percent = (dx * (x - stuff.startX) + dy * (y - stuff.startY)) / (length * length)
            distance = (dx * (y - stuff.startY) - dy * (x - stuff.startX)) / length
            return percent > 0 and percent < 1 and abs(distance) < config.hit_target_padding
        return False

    def save(self):
        d = {}
        d['nodeA'] = self.nodeA.id
        d['nodeB'] = self.nodeB.id
        if self.text:
            d['text'] = self.text
        if self.line_angle_adjust:
            d['line_angle_adjust'] = self.line_angle_adjust

        if self.parallel_part != 0.5 and self.perpendicular_part != 0:
            d['parallel_part'] = self.parallel_part
            d['perpendicular_part'] = self.perpendicular_part

        return d

    @classmethod
    def load(cls, d, nodes):
        na = None
        nb = None
        for node in nodes:
            if node.id == d['nodeA']: na = node
            elif node.id == d['nodeB']: nb = node

        self = cls(na, nb)
        if 'text' in d: self.text = d['text']
        if 'line_angle_adjust' in d: self.line_angle_adjust = d['line_angle_adjust']
        if 'parallel_part' in d: self.parallel_part = d['parallel_part']
        if 'perpendicular_part' in d: self.perpendicular_part = d['perpendicular_part']
        return self
