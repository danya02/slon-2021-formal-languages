import pygame
import node
import math
from data import Data
import config
import common_utils

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
        return Data(
            x = self.nodeA.x + dx * self.parallel_part - dy * self.perpendicular_part / scale,
            y = self.nodeA.y + dy * self.parallel_part - dx * self.perpendicular_part / scale
        )

    def set_anchor_point(self, x, y):
        dx = self.nodeB.x - self.nodeA.x
        dy = self.nodeB.y - self.nodeA.y
        scale = math.sqrt(dx*dx + dy*dy)
        self.parallelPart = (dx * (x - self.nodeA.x) + dy * (y - self.nodeA.y)) / (scale * scale)
        self.perpendicularPart = (dx * (y - self.nodeA.y) - dy * (x - self.nodeA.x)) / scale

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
                    startX = start.x
                    startY = start.y,
                    endX = end.x,
                    endY = end.y
                )

        anchor = self.get_anchor_point()
        circle = common_utils.circle_from_three_points(self.nodeA.x, self.nodeA.y, self.nodeB.x, self.nodeB.y, anchor.x, anchor.y)
        isReversed = (self.perpendicularPart > 0)
        reverseScale = 1 if is_reversed else -1
        startAngle = math.atan2(self.nodeA.y - circle.y, self.nodeA.x - circle.x) - reverseScale * nodeRadius / circle.radius
        endAngle = math.atan2(self.nodeB.y - circle.y, self.nodeB.x - circle.x) + reverseScale * nodeRadius / circle.radius
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

    def draw(self, surface):
        stuff = self.get_end_points_and_circle()
        
        # draw arc
        if stuff.has_circle:
            r = pygame.Rect(0, 0, stuff.circle_radius // 2, stuff.circle_radius // 2)
            r.centerx = stuff.centerX
            r.centery = stuff.centerY
            pygame.draw.arc(surface, pygame.Color('black'), r, c.start_angle, c.end_angle)

        else:
            pygame.draw.line( (stuff.startX, stuff.startY), (stuff.endX, stuff.endY) )

        # draw the head of the arrow
        if stuff.has_circle:
            common_utils.draw_arrow(surface, pygame.Color('black'), stuff.endX, stuff.endY, stuff.endAngle - stuff.reverseScale * (math.pi / 2))
        else:
            common_utils.draw_arrow(surface, stuff.endX, stuff.endY, math.atan2(stuff.endy - stuff.startY, stuff.endX - stuff.startX))

        # draw the text
        if stuff.has_circle:
            startAngle = stuff.start_angle
            endAngle = stuff.end_angle
            if endAngle < startAngle:
                endAngle += math.pi * 2

            textAngle = (startAngle + endAngle) / 2 + stuff.is_reversed * math.pi
            textX = stuff.circleX + stuff.circle_radius * math.cos(textAngle)
            textY = stuff.circleY + stuff.circle_radius * math.sin(textAngle)
            common_utils.draw_text(surface, self.text, textX, textY, textAngle, False)
        else:
            textX = (stuff.startX + stuff.endX) / 2
            textY = (stuff.startY + stuff.endY) / 2
            textAngle = math.atan2(stuff.endX - stuff.startX, stuff.startY - stuff.endY)
            common_utils.draw_text(surface, self.text, textX, textY, textAngle + self.line_angle_adjust, False)


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
                
                return startAngle < angle < endAngle
        else:
            dx = stuff.endX - stuff.startX
            dy = stuff.endY - stuff.startY
            length = math.sqrt(dx*dx + dy*dy)
            percent = (dx * (x - stuff.startX) + dy * (y - stuff.startY)) / (length * length)
            distance = (dx * (y - stuff.startY) - dy * (x - stuff.startX)) / length
            return percent > 0 and percent < 1 and abs(distance) < config.hit_target_padding
        return False