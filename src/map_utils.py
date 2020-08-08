#!/bin/env python3
# Map utilities

def ParseMapfile(mapfile):
    # Read and split
    m = mapfile.read().splitlines()
    tuplify = lambda string: tuple(map(int, string.split()))
    map_size, map_lines, pacman_init = tuplify(m[0]), m[1:-1], tuplify(m[-1])
    the_map = [
        [int(point) for point in row]
        for row in map_lines
    ]
    # Sanity checks
    if (len(map_lines) != map_size[1]) or (len(map_lines[0]) != map_size[0]):
        print('WARNING: inconsistent/invalid map size')
    if (the_map[pacman_init[0]][pacman_init[1]] != 0):
        print('WARNING: Pacman initial location not in empty space')
    foreign_objects = {x for each_line in the_map for x in each_line} - {0, 1, 2, 3}
    if foreign_objects != set():
        print('WARNING: foreign objects exist in map:', foreign_objects)
    return the_map, pacman_init

def GetAdjacents(the_map, x, y, filter_wall=False):
    # Sanity check
    map_y, map_x = len(the_map)-1, len(the_map[0])-1
    if (x < 0 or x > map_x) or (y < 0 or y > map_y): return None
    # Get four directions
    adjacents = []
    if (x - 1 >= 0):     adjacents.append(((x-1, y), the_map[y][x-1]))
    if (x + 1 <= map_x): adjacents.append(((x+1, y), the_map[y][x+1]))
    if (y - 1 >= 0):     adjacents.append(((x, y-1), the_map[y-1][x]))
    if (y + 1 <= map_y): adjacents.append(((x, y+1), the_map[y+1][x]))
    # Lazy check: are there walls?
    if filter_wall:
        adjacents = [each for each in adjacents if each[1] != 1]
    return adjacents

def remove_object(adjacents):
    new_adjacents = []
    for adj in adjacents:
        new_adjacents.append(adj[0])
    return new_adjacents
