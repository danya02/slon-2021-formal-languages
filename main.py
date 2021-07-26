import pygame
from node import Node
from link import Link
from self_link import SelfLink
from temp_link import TemporaryLink
from start_link import StartLink
from data import Data
import config
import random
import common_utils
import time
import yaml

pygame.init()
display = pygame.display.set_mode( (800, 600) )

nodes = [Node(50, 50), Node(100, 200), Node(200, 200)]
links = [Link(nodes[0], nodes[1]), Link(nodes[1], nodes[2])]
current_link = None
selected_object = None
moving_object = False
clock = pygame.time.Clock()

shift = False
original_click = None

caret_visible = False
caret_last_update = 0

last_click = 0
click_count = 0

def load(file):
    nodes.clear()
    links.clear()
    with open(file) as o:
        data = yaml.safe_load(o)
        for d in data.get('nodes', []):
            nodes.append(Node.load(d))
        for d in data.get('links', []):
            links.append(Link.load(d, nodes))
        for d in data.get('self_links', []):
            links.append(SelfLink.load(d, nodes))
        for d in data.get('start_links', []):
            links.append(StartLink.load(d, nodes))

def save(file):
    with open(file, 'w') as o:
        d = {}
        d['nodes'] = [i.save() for i in nodes]
        d['links'] = [i.save() for i in links if isinstance(i, Link)]
        d['self_links'] = [i.save() for i in links if isinstance(i, SelfLink)]
        d['start_links'] = [i.save() for i in links if isinstance(i, StartLink)]
        yaml.dump(d, o)



def reset_caret():
    caret_visible = True
    caret_last_update = time.time()

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

def on_key_down(key, mod, unic):
    global shift
    global selected_object
    if mod & pygame.KMOD_SHIFT:
        shift = True
    else:
        shift = False

    if key == pygame.K_DELETE:
        if selected_object is not None:
            try:
                nodes.remove(selected_object)
            except ValueError: pass
            to_remove_link = None
            to_del = []
            for l in links:
                ns = []
                try: ns.append(l.node)
                except: pass
                try: ns.append(l.nodeA)
                except: pass
                try: ns.append(l.nodeB)
                except: pass

                if l is selected_object or selected_object in ns:
                    to_del.append(l)
            for l in to_del: links.remove(l)
            selected_object = None

    elif key == pygame.K_BACKSPACE:
        if selected_object is not None:
            if 'text' in selected_object.__dict__:
                selected_object.text = selected_object.text[:-1]
                reset_caret()
    elif key == pygame.K_TAB:
        save('test.yml')
    elif key == pygame.K_ESCAPE:
        load('test.yml')
    else:
        if not (mod & pygame.KMOD_ALT) and not (mod & pygame.KMOD_CTRL) and not (mod & pygame.KMOD_META):
            if selected_object is not None:
                if 'text' in selected_object.__dict__:
                    selected_object.text += unic
                    reset_caret()


def on_key_up(key, mod):
    global shift
    if mod & pygame.KMOD_SHIFT:
        shift = True
    else:
        shift = False

while 1:
    display.fill(pygame.Color('grey'))
    for n in nodes:
        n.draw(display, selected_object, caret_visible=caret_visible and selected_object is n)
    for l in links:
        l.draw(display, selected_object, caret_visible=caret_visible and selected_object is l)
    if current_link != None:
        current_link.draw(display, selected_object, caret_visible=caret_visible)
    pygame.display.update()
#    nodes[2].x += random.randint(0, 2) - 1
#    nodes[2].y += random.randint(0, 2) - 1

    clock.tick(60)
    if time.time() - caret_last_update > 0.5:
        caret_last_update = time.time()
        caret_visible = not caret_visible

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
            on_key_down(ev.key, ev.mod, ev.unicode)
        elif ev.type == pygame.KEYUP:
            on_key_up(ev.key, ev.mod)
