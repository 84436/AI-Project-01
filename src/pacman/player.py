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

    def small_search_target(self, the_map, target, pos, is_ghost):  # target = (x, y): position of target
        if is_ghost:
            self._path = search.a_star_search(the_map, pos, target, True)
        else:
            self._path = search.a_star_search(the_map, pos, target)


    def random_move(self, the_map, init_pos):
        init_avail = the_map.get_adjacents(init_pos, False)
        current_avail = the_map.get_adjacents(self._position, False)
        if self._position != init_pos:
            init_avail.append(init_pos)
        available_moves = list(set(init_avail) & set(current_avail))
        self._path = [self._position, random.choice(available_moves)]

    def take_turn(self, the_map, food_list, is_ghost):
        if self._path:
            move = self._path.pop(0)
            self.update_position(move)
            return move
        else:
            if type(food_list) is list:
                food = food_list.pop()
                self.search_target(the_map, food, is_ghost)
            else:
                self.search_target(the_map, food_list, is_ghost)
            if self._path:
                self._path.pop(0)
                move = self._path.pop(0)
                self.update_position(move)
                return move
            else:
                return None

    def get_real_move(self, current, move):
        cur_loc = self._position
        if current[0] == move[0] and current[1] == move[1] + 1:
            return 'W', (cur_loc[0], cur_loc[1] - 1)
        if current[0] == move[0] + 1 and current[1] == move[1]:
            return 'A', (cur_loc[0] - 1, cur_loc[1])
        if current[0] == move[0] and current[1] == move[1] - 1:
            return 'S', (cur_loc[0], cur_loc[1] + 1)
        if current[0] == move[0] - 1 and current[1] == move[1]:
            return 'D', (cur_loc[0] + 1, cur_loc[1])

    def get_next_move(self):
        return self._path[0]

    def random_move_pacman(self, the_map, pos):
        ghosts = the_map.get_items(3)
        available_moves = the_map.get_adjacents(pos)
        for move in available_moves:
            temp_adj = the_map.get_adjacents(move, False)
            if list(set(ghosts) & set(temp_adj)):
                available_moves.remove(move)

        self._path = [pos, random.choice(available_moves)]

    def update_path(self, direction):
        if direction == 'W':
            for move in self._path:
                move = (move[0], move[1] - 1)
        if direction == 'A':
            for move in self._path:
                move = (move[0] - 1, move[1])
        if direction == 'S':
            for move in self._path:
                move = (move[0], move[1] + 1)
        if direction == 'D':
            for move in self._path:
                move = (move[0] + 1, move[1])


    def take_turn_lv3(self, the_map, food_list, init_pos, pos, is_ghost):
        if is_ghost:
            self.random_move(the_map, init_pos)
            self._path.pop(0)
            move = self._path.pop(0)
            self.update_position(move)
            return move
        else:      
            if len(self._path) < 2:
                temp_path = []
                for food in food_list:
                    self.small_search_target(the_map, food, pos, is_ghost)
                    temp_path.append(self._path)

                if all(v is None for v in temp_path):
                    self.random_move_pacman(the_map, pos)
                    current = self._path.pop(0)
                    move = self._path.pop(0)
                    direction, real_move = self.get_real_move(current, move)
                    self.update_position(real_move)
                    return direction, real_move

                min_len = 10000 # dirty jams
                min_index = -1
                for i in range (len(food_list)):
                    if temp_path[i] != None:
                        if len(temp_path[i]) < min_len:
                            min_len = len(temp_path[i])
                            min_index = i

                self._path = temp_path[min_index]

                current = self._path.pop(0)
                move = self._path[0]
                direction, real_move = self.get_real_move(current, move)
                self.update_position(real_move)
                return direction, real_move
            else:
                current = self._path.pop(0)
                move = self._path[0]
                direction, real_move = self.get_real_move(current, move)
                self.update_position(real_move)
                return direction, real_move


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

    #POP FOOD TO CHECK WIN

    def check_dead(self, ghost_list):
        if self.get_position() == [ghost_list[i] for i in range(len(ghost_list))]:
            return True

    def check_win(self, food_list, ghost_list):
        if len(food_list) == 0:
            return True

    def EvaluationFun(self, food_list):
        score = 0
        current_state = self.get_position()
        food_left = len(food_list)