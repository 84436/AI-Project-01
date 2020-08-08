import src.map_utils
import src.search

mapfile = open("../maps/00_21-06_dumb.txt")
the_map, pacman_init = src.map_utils.ParseMapfile(mapfile)
food = (19, 1)  # TODO: what is this?
print(src.search.a_star_search(the_map, pacman_init, food))
