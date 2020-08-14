#!/bin/env python3

from pathlib import Path        # file paths
from pacman import map_utils, player, level

# Get base dir (docs, maps, etc.)
BASE_DIR = Path(__file__).parents[1].as_posix() + '/'

# Parse map
mapfile = open(BASE_DIR + 'maps/01_19-21_macpan.txt', 'r')
the_map = map_utils.Map()
the_map.parse_file(mapfile)

# temp/test
level_1 = level.Level_1_2(the_map)
level_1.run(steps=0)
while (level_1._game_state == 0):
   input('Waiting for keypress...')
   level_1.run(steps=1)
