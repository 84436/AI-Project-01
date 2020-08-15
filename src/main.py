#!/bin/env python3
# Pacman, main file

# Built-ins
import os
import sys

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
MAP = '01_19-21_macpan.txt'
LEVEL = 1
try:
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 2:
        # Is level number valid?
        LEVEL = int(sys.argv[1])
        if LEVEL not in range(1, 2+1): raise
    elif len(sys.argv) == 3:
        # Is level number valid?
        LEVEL = int(sys.argv[1])
        if LEVEL not in range(1, 2+1): raise
        # Does this map exists?
        MAP = sys.argv[2]
        if not os.path.exists(MAPS_DIR + '/' + MAP): raise
except:
    print('ERROR: Invalid arguments/Map does not exist/Invalid level number.\nPass at most 2 arguments: [level 1-2] [mapfile.txt]. Place mapfile in ./maps folder')
    exit(-1)

################################################################################
# INIT: MAP, LEVEL AND PYGAME

# Parse map
the_map = map_utils.Map()
with open(MAPS_DIR + '/' + MAP, 'r') as mapfile:
    the_map.parse_file(mapfile)

# Create level solver
level_picker = [None, Level_1_2, Level_1_2, Level_3, Level_4]
level = level_picker[LEVEL](the_map)
print(type(level))

# PyGame: prepare images and parameters
objects = {
    WALL: pgscale(pgload(ASSETS_DIR + '/' + 'wall.png'),         (PG_OBJECT_SIZE, PG_OBJECT_SIZE)),
    FOOD: pgscale(pgload(ASSETS_DIR + '/' + 'food.png'),         (PG_OBJECT_SIZE, PG_OBJECT_SIZE)),
    GHOST: pgscale(pgload(ASSETS_DIR + '/' + 'ghost_pacman.png'), (PG_OBJECT_SIZE, PG_OBJECT_SIZE)),
    PACMAN: pgscale(pgload(ASSETS_DIR + '/' + 'pacman.png'),       (PG_OBJECT_SIZE, PG_OBJECT_SIZE)),
}
map_width, map_height = the_map.__mapsize__
window_size = [map_width * PG_OBJECT_SIZE, map_height * PG_OBJECT_SIZE]

# PyGame: init main and subsurfaces
pygame.init()
w = pygame.display
w.set_caption('Pacman')
w_loop = True
screen = w.set_mode(window_size)
surface_walls = pygame.Surface(flags=pygame.SRCALPHA, size=window_size)
surface_food = pygame.Surface(flags=pygame.SRCALPHA, size=window_size)

################################################################################

# Map: draw all (blind)
def pg_draw_all_blind():
    global the_map, screen
    screen.fill((0, 0, 0))
    for y, each_row in enumerate(the_map.__map__):
        for x, each_o in enumerate(each_row):
            if (each_o != 0):
                screen.blit(objects[each_o], (x*PG_OBJECT_SIZE, y*PG_OBJECT_SIZE))

# Surface/Walls: draw
def pg_draw_walls():
    global the_map, surface_walls
    for y, each_row in enumerate(the_map.__map__):
        for x, each_o in enumerate(each_row):
            if (each_o == WALL):
                surface_walls.blit(objects[each_o], (x*PG_OBJECT_SIZE, y*PG_OBJECT_SIZE))

# Surface/Food: draw
def pg_draw_food():
    global the_map, surface_food
    for y, each_row in enumerate(the_map.__map__):
        for x, each_o in enumerate(each_row):
            if (each_o == FOOD):
                surface_food.blit(objects[each_o], (x*PG_OBJECT_SIZE, y*PG_OBJECT_SIZE))

# Screen: draw all
def pg_draw_base(draw_mode=1):
    """Request PyGame to redraw screen\n
    `draw_mode` can be set to `0` (redraw everything) or `1` (or any other values: don't redraw walls)
    """
    global screen
    global surface_food, pg_draw_food
    if draw_mode == 0:
        global surface_walls, pg_draw_walls
        pg_draw_walls()
        screen.blit(surface_walls, (0, 0))
    pg_draw_food()
    screen.blit(surface_food, (0, 0))

# level_1 = level.Level_1_2(the_map)
# level_1.run(steps=0)
# while (level_1._game_state == 0):
#    level_1.run(steps=1)

STEP_ALL = True
STEP_DELAY = 250 # ms

pg_draw_all_blind()
while w_loop:
    # Event queue: game not over, step once
    # while level._game_state == 0 and STEP_ALL == False:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             w_loop = False
    #             break
    #     level.run()
    #     pygame.display.flip()
    
    # Event queue: game not over, step all
    while level._game_state == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                w_loop = False
                break
        level.run(steps=1)
        pg_draw_all_blind()
        pygame.display.flip()
        pygame.time.delay(STEP_DELAY)

    # Event queue: game over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            w_loop = False
            break
    pygame.display.flip()

pygame.quit()
