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
        ghost_list = the_map.get_items(2)
        if ghost_list:
            self._ghost = [player.Player(ghost_list[i]) for i in range(len(ghost_list))]
        else:
            self._ghost = [player.Player((-1, -1))]        
        # Get da food
        self._food = the_map.get_items(2)[0]
        # Turn queue for this level, ghost is unable to move to it will not be in the queue
        self._turn_queue = [self._pacman]
        # Game state: 2 = win, 1 = game over
        self._game_state = 0
        

    def update_game_state(self):
        if self._pacman.get_position() != self._food and self._pacman.get_position() not in self._map.get_items(2):
            self._pacman.update_score(False)

        if self._pacman.get_position() == self._food:
            self._pacman.update_score(True)
            self._game_state = 2

        if self._pacman.get_position() in self._map.get_items(3):
            self._game_state = 1

    def run(self, steps=-1):
        ### FIX ME

        if steps == -1:
            while self._game_state == 0:
                for each_player in self._turn_queue:
                    loc_old = each_player.get_position()
                    move = each_player.take_turn(self._map, self._food, False)
                    if not move:
                        self._game_state = 2
                        break
                    self._map.move_player(loc_old, move)
                    self.update_game_state()
                    if self._game_state != 0:
                        break
        else:
            for _ in range(steps):
                if self._game_state == 0:
                    for each_player in self._turn_queue:
                        loc_old = each_player.get_position()
                        move = each_player.take_turn(self._map, self._food, False)
                        if not move:
                            self._game_state = 2
                            break
                        self._map.move_player(loc_old, move)
                        self.update_game_state()
                        if self._game_state != 0:
                            break
