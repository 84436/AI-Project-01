import src.map_utils
import src.Player


map_file = open("../maps/00_21-06_dumb.txt")
the_map, pacman_init = src.map_utils.ParseMapfile(map_file)
food = (19, 1)

pacman = src.Player.Pacman(pacman_init, 0)
pacman.search_target(the_map, food)
print(pacman.get_path())
