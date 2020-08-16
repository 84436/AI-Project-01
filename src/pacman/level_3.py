# Level-specific solvers
from . import player, map_utils, search
import random


class Level_3:
    def __init__(self, the_map):
        # Get da map
        self._map = the_map
        # Get da pacman
        self._pacman = player.Pacman(the_map.get_items(9), 0)
        # Get da ghost
        self._init_ghost = the_map.get_items(3)
        if self._init_ghost:
            self._ghost = [player.Player(self._init_ghost[i]) for i in range(len(self._init_ghost))]
        else:
            self._ghost = player.Player((-1, -1))
        # Get da food
        self._food = the_map.get_items(2)
        # Turn queue for this level
        self._turn_queue = [self._pacman]
        self._turn_queue += self._ghost
        # Game state: 2 = win, 1 = game over
        self._game_state = 0

        self._max_iter = 500 # =))))))))

    def update_game_state(self, pacman_turn):
        if pacman_turn: 
            self._pacman.update_score(False)

        if self._pacman.get_position() in self._food and pacman_turn:
            self._pacman.update_score(True)
            self._food.remove(self._pacman.get_position())
            self._game_state = 3  # got food

        if not self._food:
            self._game_state = 2

        try:
            if self._map.get_items(9) in self._map.get_items(3):
                self._game_state = 1
        except IndexError:
            self._game_state = 1        

    def run(self, steps=-1):
        if steps == -1:
            direction = None
            while self._game_state == 0 and self._max_iter != 0:
                self._max_iter -= 1
                slice_map = None
                move = None
                turn = False  # not pacman
                pacman_food_list = []
                for index, each_player in enumerate(self._turn_queue):
                    loc_old = each_player.get_position()
                        
                    if type(each_player).__name__ == "Pacman":
                        turn = True
                    else: 
                        turn = False

                    if turn:
                        slice_map = self._map.get_map_slice(each_player.get_position())  # pacman POV
                        small_pacman = slice_map.get_items(9)
                        pacman_food_list = slice_map.get_items(2)

                        if each_player._path and (each_player.get_next_move() in self._map.get_items(3) or each_player.get_next_move() is None):
                            each_player._path = []
                        direction, move = each_player.take_turn_lv3(slice_map, pacman_food_list, None, small_pacman, False)
                    else:
                        ghost_index = index - 1
                        move = each_player.take_turn_lv3(self._map, None, self._init_ghost[ghost_index], None, True)

                    self._map.move_player(loc_old, move)
                    self.update_game_state(turn)

                    if self._game_state != 0 and self._game_state != 3:
                        break

                    if self._game_state == 3:
                        self._game_state = 0
                        each_player._path = []
                        continue
                    
                    if turn:
                        each_player.update_path(direction)

        else:
            for _ in range(steps):
                if self._game_state == 0 and self._max_iter != 0:
                    self._max_iter -= 1
                    slice_map = None
                    move = None
                    turn = False  # not pacman
                    pacman_food_list = []
                    for index, each_player in enumerate(self._turn_queue):
                        loc_old = each_player.get_position()
                            
                        if type(each_player).__name__ == "Pacman":
                            turn = True
                        else: 
                            turn = False

                        if turn:
                            slice_map = self._map.get_map_slice(each_player.get_position())  # pacman POV
                            small_pacman = slice_map.get_items(9)
                            pacman_food_list = slice_map.get_items(2)

                            if each_player._path and each_player.get_next_move() in self._map.get_items(3):
                                each_player._path = []
                            direction, move = each_player.take_turn_lv3(slice_map, pacman_food_list, None, small_pacman, False)
                        else:
                            ghost_index = index - 1
                            move = each_player.take_turn_lv3(self._map, None, self._init_ghost[ghost_index], None, True)

                        self._map.move_player(loc_old, move)
                        self.update_game_state(turn)

                        if self._game_state != 0 and self._game_state != 3:
                            break

                        if self._game_state == 3:
                            self._game_state = 0
                            each_player._path = []
                            continue
                        
                        if turn:
                            each_player.update_path(direction)
