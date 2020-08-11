#!/bin/env python3

from pathlib import Path        # file paths
from src.pacman import map_utils, player, level

# Get base dir (docs, maps, etc.)
BASE_DIR = Path(__file__).parents[1].as_posix() + '/'

# Parse map
mapfile = open(BASE_DIR + 'maps/00_21-06_dumb.txt', 'r')
the_map = map_utils.Map()
the_map.parse_file(mapfile)

# temp/test
food = the_map.get_items(2)[0]
pacman_init = the_map.get_items(9)

pacman_1 = player.Pacman(pacman_init, 0)
level_1 = level.Level_1(the_map, pacman_1, food)
level_1.run()
