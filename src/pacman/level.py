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
                self._map.move_player(self._pacman.get_position(), move)
                self._pacman.update_position(move)
                self._pacman.update_score(False)
            self._map.remove_food(self._food)

        if self._pacman.get_position() == self._food:
            self._pacman.update_score(True)

# class Level_2:
#     def __init__(self, the_map, pacman, ghost, food):
