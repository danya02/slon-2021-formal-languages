import pygame
import common_utils
import config
from data import Data

class StartLink:
    def __init__(self, node, start):
        self.node = node
        self.deltaX = 0
        self.deltaY = 0
        self.text = ''
        if start:
            self.setAnchorPoint(start.x, start.y)

    def set_anchor_point(self, x, y):
        self.deltaX = x - self.node.x
        self.deltaY = y - self.node.y

        if abs(self.deltaX) < config.snapToPadding: self.deltaX = 0
        if abs(self.deltaY) < config.snapToPadding: self.deltaY = 0

    def get_end_points(self):
        startX = self.node.x + self.deltaX
        startY = self.node.y + self.deltaY
        end = self.node.closest_point_on_circle(startX, startY)
        return Data(startX=startX, startY=startY, endX=endX, endY=endY)

    def draw(self, surface, selected_object, caret_visible=None, **kwargs):
        c = common_utils.get_color(self, selected_object)
        stuff = self.get_end_points()

        # draw the line
        pygame.draw.line( surface, c, (stuff.startX, stuff.startY), (stuff.endX, stuff.endY) )

        # draw the text at the end without the arrow
        text_angle = math.atan2(stuff.startY - stuff.endY, stuff.startX - stuff.EndX)
        common_utils.draw_text(surface, self.text, stuff.startX, stuff.startY, textAngle, c, caret_visible)

        # draw the head of the arrow
        common_utils.draw_arrow(surface, stuff.endX, stuff.endY, math.atan2(-self.deltaY, self.deltaX), c)

    def contains_point(self, x, y):
        stuff = self.get_end_points()
        dx = stuff.endX - stuff.startX
        dy = stuff.endY - stuff.startY
        length = math.sqrt(dx*dx + dy*dy);
        percent = (dx * (x - stuff.startX) + dy * (y - stuff.startY)) / (length * length)
        distance = (dx * (y - stuff.startY) - dy * (x - stuff.startX)) / length
        return (percent > 0 and percent < 1 && abs(distance) < config.hitTargetPadding)
