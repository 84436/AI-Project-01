#!/bin/env python3
# Map drawing using PyGame

import pygame
import copy
import threading
from . import map_utils

# Read the map
# mapfile = open('../../maps/01_19-21_macpan.txt', 'r')
# m = map_utils.Map()
# m.parse_file(mapfile)

class MapDrawer:
    def __init__(self, the_map):
        # Object init
        self.object_size = 24
        self.object_1_wall = pygame.image.load('../assets/wall.png')
        self.object_2_food = pygame.image.load('../assets/food.png')
        self.object_3_ghost = pygame.image.load('../assets/ghost_pacman.png')
        self.object_9_pacman = pygame.image.load('../assets/pacman.png')
        self.objects = {
            1: pygame.transform.scale(self.object_1_wall, (self.object_size, self.object_size)),
            2: pygame.transform.scale(self.object_2_food, (self.object_size, self.object_size)),
            3: pygame.transform.scale(self.object_3_ghost, (self.object_size, self.object_size)),
            9: pygame.transform.scale(self.object_9_pacman, (self.object_size, self.object_size)),
        }

        # Map init
        self.map_width, self.map_height = the_map.__mapsize__
        self.window_size = [self.map_width * self.object_size, self.map_height * self.object_size]

        # PyGame init
        pygame.init()
        self.w = pygame.display
        self.w.set_caption('Pacman')
        self.screen = self.w.set_mode(self.window_size)

    def draw(self, the_map):
        self.screen.fill((0, 0, 0))
        for y, each_row in enumerate(the_map.__map__):
            for x, each_o in enumerate(each_row):
                if (each_o != 0):
                    self.screen.blit(self.objects[each_o], (x*self.object_size, y*self.object_size))
        self.w.update()
    
    def destroy(self):
        pygame.quit()
