import src.search
import src.map_utils
import random


class Player:
    def __init__(self, position):
        self._position = position
        self._path = []

    def get_position(self):
        return self._position

    def get_path(self):
        return self._path

    def search_target(self, the_map, target):  # target = (x, y): position of target
        self._path = src.search.a_star_search(the_map, self._position, target)

    def random_move(self, the_map):
        available_moves = src.map_utils.GetAdjacents(the_map, self._position[0], self._position[1], True)
        self._path = [self._position, random.choice(available_moves)]


class Pacman(Player):
    def __init__(self, position, score):
        super().__init__(position)
        self._score = score

    def get_score(self):
        return self._score

    def update_score(self, move_score):
        self._score = self._score + move_score
