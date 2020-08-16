from . import player


class Level_4:
    def __init__(self, the_map):
        # Get da map
        self._map = the_map
        # Get da pacman
        self._pacman = player.Pacman(the_map.get_items(9), 0)
        # Get da ghost
        ghost_list = the_map.get_items(3)

        self._ghost = [player.Player(ghost_list[i]) for i in range(len(ghost_list))]
        self._food_list = the_map.get_items(2)
        # Turn queue for this level, ghost is unable to move to it will not be in the queue
        self._turn_queue = [self._pacman]
        self._turn_queue += self._ghost
        # Game state: 2 = win, 1 = game over
        self._game_state = 0

    def update_game_state(self):
        if self._pacman.get_position() != [self._food_list[i] for i in
                                           range(len(self._food_list))] and self._pacman.get_position() != [
            self._ghost[i] for i in range(len(self._ghost))]:
            self._pacman.update_score(False)

        # accident meet other food than target
        if self._pacman.get_position() == [self._food_list[i] for i in range(len(self._food_list))]:
            self._pacman.update_score(True)
            self._food_list.remove(self._pacman.get_position())

        if self._pacman.check_win(food_list=self._food_list):
            self._game_state = 2

        if self._pacman.check_dead(ghost_list=self._ghost):
            self._game_state = 1

    def run(self, steps=-1):
        ### FIX ME

        if steps == -1:
            while self._game_state == 0:
                for each_player in self._turn_queue:
                    loc_old = each_player.get_position()
                    if type(each_player) is player.Pacman:
                        move = each_player.take_turn_lv4(self._map, self._food_list, False)
                    else:
                        move = each_player.take_turn(self._map, self._pacman.get_position(), True)
                    if not move:
                        self._game_state = 2
                        break
                    self._map.move_player(loc_old, move)
                    self.update_game_state()
                    # Redraw map
                    if self._game_state != 0:
                        break
        else:
            for _ in range(steps):
                if self._game_state == 0:
                    for each_player in self._turn_queue:
                        loc_old = each_player.get_position()
                        if type(each_player) is player.Pacman:
                            move = each_player.take_turn_lv4(self._map, self._food_list, False)
                        else:
                            move = each_player.take_turn(self._map, self._pacman.get_position(), True)
                        if not move:
                            self._game_state = 2
                            break
                        self._map.move_player(loc_old, move)
                        self.update_game_state()
                        if self._game_state != 0:
                            break
                        print(type(each_player).__name__)
