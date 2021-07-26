import pygame
import common_utils
import math

class TemporaryLink:
    def __init__(self, from_, to):
        self.from_ = from_
        self.to = to

    def draw(self, surface, selected_object, **kwargs):
        c = common_utils.get_color(self, selected_object, **kwargs)

        # draw the line
        pygame.draw.line(surface, c,  (self.from_.x, self.from_.y), (self.to.x, self.to.y) )

        # draw the head of the arrow
        common_utils.draw_arrow(surface, self.to.x, self.to.y, math.atan2(self.to.y - self.from_.y, self.to.x - self.from_.x), c)
