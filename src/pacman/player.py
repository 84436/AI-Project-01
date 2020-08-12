#!/bin/env python3
# Pacman and Ghosts

from . import map_utils, search
import random

class Player:
    def __init__(self, position):
        self._position = position
        self._path = []

    def get_position(self):
        return self._position

    def get_path(self):
        return self._path

    def update_position(self, position):
        self._position = position

    def search_target(self, the_map, target, is_ghost):  # target = (x, y): position of target
        if is_ghost:
            self._path = search.a_star_search(the_map, self._position, target, True)
        else:
            self._path = search.a_star_search(the_map, self._position, target)

    def random_move(self, the_map):
        available_moves = the_map.get_adjacents(self._position)
        self._path = [self._position, random.choice(available_moves)]

    def take_turn(self, the_map, move):
        the_map.move_player(self.get_position(), move)
        self.update_position(move)

class Pacman(Player):
    def __init__(self, position, score):
        super().__init__(position)
        self._score = score

    def get_score(self):
        return self._score

    def update_score(self, is_food):
        if is_food:
            self._score = self._score + 20
        else:
            self._score = self._score - 1
