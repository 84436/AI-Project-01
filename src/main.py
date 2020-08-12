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
level_1 = level.Level_1_2(the_map)
level_1.run()
