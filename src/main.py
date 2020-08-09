import src.map_utils
import src.Player
import src.Level


map_file = open("../maps/00_21-06_dumb.txt")
the_map, pacman_init = src.map_utils.ParseMapfile(map_file)
food = (19, 1)

pacman = src.Player.Pacman(pacman_init, 0)
level_1 = src.Level.Level_1(the_map, pacman, food)
level_1.run()
