import pygame
import math
import config
import common_utils
import config
from data import Data

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0
        self.is_accept_state = False
        self.text = ''

    def set_mouse_start(self, x, y):
        self.mouse_offset_x = self.x - x
        self.mouse_offset_y = self.y - y
    
    def set_anchor_point(self, x, y):
        self.x = x + self.mouse_offset_x
        self.y = y + self.mouse_offset_y

    def draw(self, surface, selected_object, caret_visible=None, **kwargs):
        c = common_utils.get_color(self, selected_object)
        # draw the circle
        pygame.draw.circle(surface, c, (self.x, self.y), config.node_radius, 1)

        # draw the text
        common_utils.draw_text(surface, self.text, self.x, self.y, None, c, caret_visible)

        # draw a double circle for the accept state
        if self.is_accept_state:
            pygame.draw.circle(surface, c, (self.x, self.y), config.node_radius - 6, 1)

        
    def closest_point_on_circle(self, x, y):
        dx = x - self.x
        dy = y - self.y
        scale = math.sqrt(dx*dx + dy*dy)
        return Data(
            x = self.x + dx * config.node_radius / scale,
            y = self.y + dy * config.node_radius / scale
        )


    def contains_point(self, x, y):
        return (x - self.x)*(x - self.x) + (y - self.y)*(y - self.y) < config.node_radius*config.node_radius
