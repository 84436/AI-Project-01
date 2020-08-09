#!/bin/env python3
# Level-specific solvers

from . import player, map_utils

class Level_1:
    def __init__(self, the_map, pacman, food):
        self._map = the_map
        self._pacman = pacman
        self._food = food

    def run(self):
        self._pacman.search_target(self._map, self._food)
        path = self._pacman.get_path()
        if path:
            for move in path:
                map_utils.update_map(self._map, self._pacman.get_position(), move)
                self._pacman.update_position(move)
                self._pacman.update_score(-1)
                map_utils.print_map(self._map)
            self._pacman.update_score(20)

        print(self._pacman.get_score())
