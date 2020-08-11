#!/bin/env python3
# Level-specific solvers

from . import player

class Level_1_2:
    def __init__(self, the_map):
        # Get da map
        self._map = the_map
        # Get da pacman
        self._pacman = player.Pacman(the_map.get_items(9), 0)
        # Get da ghost
        ghost_list = the_map.get_items(2)[0]
        if ghost_list:
            self._ghost = player.Player(ghost_list[0])
        else:
            self._ghost = player.Player((-1, -1))
        # Get da food
        self._food = the_map.get_items(2)[0]
        # Turn queue for this level, ghost is unable to move to it will not be in the queue
        self._turn_queue = [self._pacman]
        # Game state: 2 = win, 1 = game over
        self._game_state = 0

    def run(self):
        self._pacman.search_target(self._map, self._food, False)
        path = self._pacman.get_path()

        while (self._game_state != 1 or self._game_state != 2) and path:
            for each_player in self._turn_queue:
                each_player.take_turn(self._map, path.pop(0))

                if self._pacman.get_position() != self._food and self._pacman.get_position() != self._ghost.get_position():
                    self._pacman.update_score(False)

                if self._pacman.get_position() == self._food:
                    self._pacman.update_score(True)
                    self._game_state = 2
                    break

                if self._pacman.get_position() == self._ghost.get_position():
                    self._game_state = 1
                    break

        game_state = 2
        