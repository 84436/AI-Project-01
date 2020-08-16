#!/bin/env python3
# Pacman, main file

# Built-ins
import os
import sys

# Supress PyGame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# External: PyGame (for drawing)
import pygame
pgload = pygame.image.load
pgscale = pygame.transform.scale

# Local: utilities
from pacman import map_utils, player
# Local: levels
from pacman.level_1_2 import *
from pacman.level_3 import *
from pacman.level_4 import *

################################################################################
# WORKING DIRECTORIES, ARGUMENTS AND CONSTANTS

# Constants
PG_OBJECT_SIZE = 24
STEP_DELAY = 100 # ms

# Objects
WALL = 1
FOOD = 2
GHOST = 3
PACMAN = 9

# Get base dir (docs, maps, etc.)
BASE_DIR   = os.path.dirname(os.path.realpath(__file__)) + '/..'
ASSETS_DIR = BASE_DIR + '/assets'
MAPS_DIR   = BASE_DIR + '/maps'

# Set maps and levels (from default or from arguments)
MAP = 'macpan'
LEVEL = 3
try:
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 2:
        # Is level number valid?
        LEVEL = int(sys.argv[1])
        if LEVEL not in range(1, 4+1): raise
    elif len(sys.argv) == 3:
        # Is level number valid?
        LEVEL = int(sys.argv[1])
        if LEVEL not in range(1, 4+1): raise
        # Does this map exists?
        MAP = sys.argv[2]
        if not os.path.exists(MAPS_DIR + '/' + MAP + '.txt'): raise
except:
    print('ERROR: Invalid arguments/Map does not exist/Invalid level number.\nPass at most 2 arguments: [level 1-2] [mapfile (no extension)]. Place mapfile.txt in ./maps folder')
    exit(-1)

################################################################################
# INIT: MAP, LEVEL AND PYGAME

# Parse map
the_map = map_utils.Map()
with open(MAPS_DIR + '/' + MAP + '.txt', 'r') as mapfile:
    the_map.parse_file(mapfile)

# Create level solver
level_picker = [None, Level_1_2, Level_1_2, Level_3, Level_4]
level = level_picker[LEVEL](the_map)

# PyGame: prepare images and parameters
objects = {
    WALL: pgscale(pgload(ASSETS_DIR + '/' + 'wall.png'),         (PG_OBJECT_SIZE, PG_OBJECT_SIZE)),
    FOOD: pgscale(pgload(ASSETS_DIR + '/' + 'food.png'),         (PG_OBJECT_SIZE, PG_OBJECT_SIZE)),
    GHOST: pgscale(pgload(ASSETS_DIR + '/' + 'ghost_pacman.png'), (PG_OBJECT_SIZE, PG_OBJECT_SIZE)),
    PACMAN: pgscale(pgload(ASSETS_DIR + '/' + 'pacman.png'),       (PG_OBJECT_SIZE, PG_OBJECT_SIZE)),
}
map_width, map_height = the_map.__mapsize__
control_bar_height = 48 + 2*8
window_size = [map_width * PG_OBJECT_SIZE, map_height * PG_OBJECT_SIZE + control_bar_height]

# PyGame: init main and subsurfaces
pygame.init()
w = pygame.display
w.set_caption('Pacman')
w_loop = True
screen = w.set_mode(window_size)
surface_walls = pygame.Surface(flags=pygame.SRCALPHA, size=window_size)
surface_food = pygame.Surface(flags=pygame.SRCALPHA, size=window_size)

# Map: draw all (blind)
def pg_draw_all_blind():
    global the_map, screen
    screen.fill((0, 0, 0))
    for y, each_row in enumerate(the_map.__map__):
        for x, each_o in enumerate(each_row):
            if (each_o != 0):
                screen.blit(objects[each_o], (x*PG_OBJECT_SIZE, y*PG_OBJECT_SIZE))

################################################################################
# CONTROL BUTTONS FOR MAIN LOOP
# https://pythonprogramming.net/pygame-button-function-events
# https://stackoverflow.com/questions/47639826/pygame-button-single-click

# Buttons
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 48
button_score = {
    'rect': (0*BUTTON_WIDTH + (0+1)*8, (map_height * PG_OBJECT_SIZE) + 8, BUTTON_WIDTH, BUTTON_HEIGHT),
    'color_active': (0, 255, 255),
    'color_inactive': (0, 255, 255),
    'text': '',
    'action': None
}
button_step_once = {
    'rect': (1*BUTTON_WIDTH + (1+1)*8, (map_height * PG_OBJECT_SIZE) + 8, BUTTON_WIDTH, BUTTON_HEIGHT),
    'color_active': (0, 255, 0),
    'color_inactive': (0, 127, 0),
    'text': '> Step 1',
    'action': 'step_once'
}
button_step_all = {
    'rect': (2*BUTTON_WIDTH + (2+1)*8, (map_height * PG_OBJECT_SIZE) + 8, BUTTON_WIDTH, BUTTON_HEIGHT),
    'color_active': (0, 255, 0),
    'color_inactive': (0, 127, 0),
    'text': '>>> Step all',
    'action': 'step_all'
}
buttons = [button_step_once, button_step_all]

# Font for button
FONT_FILE = ASSETS_DIR + '/Inconsolata-Regular.ttf'
font = pygame.font.Font(FONT_FILE, 16)

# Button drawer
def draw_button(rect, color, text):
    global screen
    bx, by, bw, bh = rect
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(int(bx+(bw/2)), int(by+(bh/2))))
    screen.blit(text_surface, text_rect)

################################################################################
# MAIN LOOP

# Print basic info
print('Level = {l}\nMap   = {m} ({mx} * {my} tiles)\nCtrl-C here to stop.'.format(
    l = LEVEL,
    m = MAP,
    mx = the_map.__mapsize__[1],
    my = the_map.__mapsize__[0]
))

STEP_ALL = False
GAME_OVER_PRINT_MSG = False

while w_loop:
    # Mode: step once
    while level._game_state == 0 and STEP_ALL == False:
        # Draw map
        pg_draw_all_blind()
        # Draw score
        draw_button(button_score['rect'], button_score['color_active'], str(level._pacman._score))
        # Draw button (with mouseover detection)
        for each_button in buttons:
            if pygame.Rect(each_button['rect']).collidepoint(pygame.mouse.get_pos()):
                draw_button(each_button['rect'], each_button['color_active'], each_button['text'])
            else:
                draw_button(each_button['rect'], each_button['color_inactive'], each_button['text'])
        # Handle event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            # One of the buttons is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for each_button in buttons:
                    if pygame.Rect(each_button['rect']).collidepoint(pygame.mouse.get_pos()):
                        if each_button['action'] == 'step_once':
                            level.run(steps=1)
                        elif each_button['action'] == 'step_all':
                            print('Step all mode activated.')
                            STEP_ALL = True
        w.update()
    
    # Mode: step all
    while level._game_state == 0:
        # Draw map
        pg_draw_all_blind()
        # Draw score
        draw_button(button_score['rect'], button_score['color_active'], str(level._pacman._score))
        # Run
        level.run(steps=1)
        # Handle event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        w.update()
        pygame.time.delay(STEP_DELAY)

    # Mode: game over
    # Print game over message (once)
    if not GAME_OVER_PRINT_MSG:
        if level._game_state == 1:
            print('Game over: Pacman lost.')
        else: # level._game_state == 2:
            print('Game over: Pacman won.')
        GAME_OVER_PRINT_MSG = True
    # Draw map
    pg_draw_all_blind()
    # Draw score
    draw_button(button_score['rect'], button_score['color_active'], str(level._pacman._score))
    # Handle event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    w.update()

pygame.quit()
