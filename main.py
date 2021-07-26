import pygame
from node import Node
from link import Link
from self_link import SelfLink
from temp_link import TemporaryLink
from data import Data
import config
import random
import common_utils
import time

pygame.init()
display = pygame.display.set_mode( (800, 600) )

nodes = [Node(50, 50), Node(100, 200), Node(200, 200)]
links = [Link(nodes[0], nodes[1]), Link(nodes[1], nodes[2])]
current_link = None
selected_object = None
moving_object = False
clock = pygame.time.Clock()

shift = False

#links[1].set_anchor_point(random.randint(0, 800), random.randint(0, 600))

links[1].set_anchor_point(200, 300)
original_click = None

last_click = 0
click_count = 0

def reset_caret(): pass

def on_mouse_down(x,y):
    global original_click
    global current_link
    global selected_object
    global moving_object
    global last_click
    global click_count
    selected_object = common_utils.select_object(x, y, nodes, links)
    moving_object = False
    mouse = Data(x=x, y=y)
    original_click = mouse
    
    click_duration = time.time() - last_click
    last_click = time.time()

    if click_duration < config.double_click_seconds:
        click_count += 1
        if click_count >= 2:
            on_double_click(x, y)
            click_count = 0
    else:
        click_count = 0

    print(selected_object)
    if selected_object is not None:
        if shift and isinstance(selected_object, Node):
            current_link = SelfLink(selected_object, mouse)
        else:
            moving_object = True
            delta_mouse_x = delta_mouse_y = 0
            if 'set_mouse_start' in selected_object.__dict__:
                selected_object.set_mouse_start(x, y)

        reset_caret()

    elif shift:
        current_link = TemporaryLink(mouse, mouse)


def on_mouse_move(x, y):
    global current_link
    global target_node
    global moving_object
    global original_click
    mouse = Data(x=x, y=y)
    if current_link is not None:
        target_node = common_utils.select_object(x, y, nodes)
        if not isinstance(target_node, Node):
            target_node = None

        if selected_object is None:
            if target_node is not None:
                current_link = StartLink(target_node, original_click)
            else:
                current_link = TemporaryLink(original_click, mouse)
        else:
            if target_node is selected_object:
                current_link = SelfLink(selected_object, mouse)
            elif target_node is not None:
                current_link = Link(selected_object, target_node)
            else:
                current_link = TemporaryLink(selected_object.closest_point_on_circle(x, y), mouse)

    if moving_object:
        selected_object.set_anchor_point(x, y)
        if isinstance(selected_object, Node):
            common_utils.snap_node(selected_object, nodes)

def on_mouse_up(x, y):
    global moving_object
    global current_link

    moving_object = False
    if current_link is not None:
        if not isinstance(current_link, TemporaryLink):
            selected_object = current_link
            links.append(current_link)
            reset_caret()
        current_link = None

def on_double_click(x, y):
    global selected_object
    selected_object = common_utils.select_object(x, y, nodes, links)
    
    if selected_object is None:
        selected_object = Node(x, y)
        nodes.append(selected_object)
        reset_caret()
    elif isinstance(selected_object, Node):
        selected_object.is_accept_state = not selected_object.is_accept_state

def on_key_down(key, mod):
    global shift
    if mod & pygame.KMOD_SHIFT:
        shift = True
    else:
        shift = False

def on_key_down(key, mod):
    global shift
    if mod & pygame.KMOD_SHIFT:
        shift = True
    else:
        shift = False

def on_key_up(key, mod):
    global shift
    if mod & pygame.KMOD_SHIFT:
        shift = True
    else:
        shift = False

while 1:
    display.fill(pygame.Color('grey'))
    for n in nodes:
        n.draw(display)
    for l in links:
        l.draw(display)
    if current_link != None:
        current_link.draw(display)
    pygame.display.update()
    nodes[2].x += random.randint(0, 2) - 1
    nodes[2].y += random.randint(0, 2) - 1

    clock.tick(60)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            raise SystemExit
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            on_mouse_down(*ev.pos)
        elif ev.type == pygame.MOUSEMOTION:
            on_mouse_move(*ev.pos)
        elif ev.type == pygame.MOUSEBUTTONUP:
            on_mouse_up(*ev.pos)
        elif ev.type == pygame.KEYDOWN:
            on_key_down(ev.key, ev.mod)
        elif ev.type == pygame.KEYUP:
            on_key_up(ev.key, ev.mod)
