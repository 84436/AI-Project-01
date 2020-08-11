# Level-specific solvers
from . import player, map_utils
from . import map_utils, search
import random


class Level_3:
    explored_node = []
    queue = []
    def __init__(self, the_map, pacman, ghost, food):
        self._map = the_map
        self._pacman = pacman
        self._food = food
        self._ghost = ghost
    def run(self):

