import pygame
import math
from data import Data
import common_utils

class SelfLink:
    def __init__(self, node, mouse=None):
        self.node = node
        self.anchor_angle = 0
        self.mouse_offset_angle = 0
        self.text = ''
        if mouse:
            self.set_anchor_point(mouse.x, mouse.y)

    def set_mouse_start(self, x, y):
        self.mouse_offset_angle = self.anchor_angle - math.atan2(y - self.node.y, x - self.node.x) + self.mouse_offset_angle

        # snap to 90 degres
        snap = math.round(self.anchor_angle / (math.pi / 2)) * (math.pi / 2)
        if abs(self.anchor_angle - snap) < 0.1): self.anchor_angle = snap

        # keep in the range -pi to pi so our contains_point() function always works
        if self.anchor_angle < -math.pi: self.anchor_angle += 2*math.pi
        if self.anchor_angle > math.pi: self.anchor_angle -= 2*math.pi

    def get_end_points_and_circle(self):
        circleX = self.node.x + 1.5 * config.node_radius * math.cos(self.anchor_angle)
        circleY = self.node.y + 1.5 * config.node_radius * math.sin(self.anchor_angle)
        circleRadius = 0.75 * config.node_radius
        startAngle = self.anchor_angle - math.pi * 0.8
        endAngle = self.anchor_angle + math.pi * 0.8
        startX = circleX + circleRadius * math.cos(startAngle)
        startY = circleY + circleRadius * math.sin(startAngle)
        endX = circleX + circleRadius * math.cos(endAngle)
        endY = circleY + circleRadius * math.sin(endAngle)
        return Data(
            has_circle = True,
            startX = startX,
            startY = startY,
            endX = endX,
            endY = endY,
            start_angle = startAngle,
            end_angle = endAngle,
            circleX = circleX,
            circleY = circleY,
            circle_radius = circleRadius
        )

    def draw(self, surface):
        stuff = self.get_end_points_and_circle()
        
        # draw arc
        r = pygame.Rect(0, 0, stuff.circle_radius*2, stuff.circle_radius*2)
        r.centerx = stuff.centerX
        r.centery = stuff.centerY
        pygame.draw.arc(surface, pygame.Color('black'), r, self.start_angle, self.end_angle)

        # draw the text on the loop farthest from the node
        textX = stuff.circleX + stuff.circle_radius * math.cos(self.anchorAngle);
        textY = stuff.circleY + stuff.circle_radius * math.sin(self.anchorAngle);
        common_utils.draw_text(surface, self.text, textX, textY, self.anchor_angle, False)

        # draw the head of the arrow
        common_utils.draw_arrow(surface, stuff.endX, stuff.endY, stuff.end_angle + math.pi * 0.4)

    def contains_point(self, x, y):
        stuff = self.get_end_points_and_circle()
        dx = x - stuff.circleX
        dy = y - stuff.circleY
        distance = math.sqrt(dx*dx + dy*dy) - stuff.circle_radius
        return abs(distance) < config.hit_target_padding
