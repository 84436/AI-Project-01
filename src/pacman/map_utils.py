#!/bin/env python3
# Map utilities

class Map:
    def __init__(self, init_map=None):
        """Create a new empty map, or import from a 2D array (`init_map`)
        """

        # Utility for parse_map: str --> tuple(int, int)
        self.__tuplify__ = lambda string: tuple(map(int, string.split()))
        
        # Import from existing map...
        if init_map:
            self.__map__ = init_map
            self.__mapsize__ = (len(self.__map__[0]), len(self.__map__))
        # ...or create an empty one
        else:
            self.__map__ = None
            self.__mapsize__ = None
    
    def __inmap(self, x, y):
        """Check if a given point is within the map.
        """
        return (
            x in range(0, self.__mapsize__[0]) and
            y in range(0, self.__mapsize__[1])
        )

    def __getitem__(self, loc):
        return self.__map__[loc[1]][loc[0]]

    def __setitem__(self, loc, item):
        self.__map__[loc[1]][loc[0]] = item

    def __str__(self):
        return '\n'.join([
            ' '.join(str(x) for x in row)
            for row in self.__map__
        ])
    
    def parse_file(self, mapfile):
        """Parse a mapfile.
        """

        # Read and split
        m = mapfile.read().splitlines()
        self.__mapsize__, map_lines, pacman_init = self.__tuplify__(m[0]), m[1:-1], self.__tuplify__(m[-1])
        self.__mapsize__ = (self.__mapsize__[1], self.__mapsize__[0])
        self.__map__ = [
            [int(point) for point in row]
            for row in map_lines
        ]
        
        # Sanity checks
        if (len(map_lines) != self.__mapsize__[1]) or (len(map_lines[0]) != self.__mapsize__[0]):
            print('WARNING: inconsistent/invalid map size')
        if (self[pacman_init] != 0):
            print('WARNING: Pacman initial location not in empty space')
        foreign_objects = {x for each_line in self.__map__ for x in each_line} - {0, 1, 2, 3}
        if foreign_objects != set():
            print('WARNING: foreign objects exist in map:', foreign_objects)
        
        # Set Pacman location
        self[pacman_init] = 9
    
    def get_map_slice(self, loc, foresight=3):
        """Get a partial map from a location.
        """

        # Sanity check
        x, y = loc
        map_x, map_y = self.__mapsize__
        if not self.__inmap(x, y): return None

        # Get the boundaries
        bxleft  = max(0,     x - foresight)
        bxright = min(map_x, x + foresight)
        byup    = max(0,     y - foresight)
        bydown  = min(map_y, y + foresight)

        # Slice the map
        sliced_map = [
            row[bxleft:bxright+1]
            for row in self.__map__[byup:bydown+1]
        ]
        return Map(init_map=sliced_map)

    def get_adjacents(self, loc, filter_ghost=True):
        """Get adjacent nodes.\n\n
        """

        # Sanity check
        x, y = loc
        if not self.__inmap(x, y): return None

        # Get four directions
        adjacents = []
        if self.__inmap(x-1, y) : adjacents.append(((x-1, y)))
        if self.__inmap(x+1, y) : adjacents.append(((x+1, y)))
        if self.__inmap(x, y-1) : adjacents.append(((x, y-1)))
        if self.__inmap(x, y+1) : adjacents.append(((x, y+1)))

        # Filter all walls
        adjacents = [each for each in adjacents if self[each] != 1]
        # Pacman: filter all Ghosts
        if filter_ghost:
            adjacents = [each for each in adjacents if self[each] != 3]
        return adjacents

    def get_items(self, item):
        """Get the location of items in map.\n\n
        Allowed items: `2` (food), `3` (Ghost), `9` (Pacman).\n\n
        Returns: direct location (for `9`) or list of locations (for `2` and `3`).
        """

        # Sanity check
        if item not in [2, 3, 9]:
            return None
        
        # Get the items
        r = [
            (x, y)
            for y, row in enumerate(self.__map__)
            for x, item_in_map in enumerate(row)
            if item_in_map == item
        ]

        # Hack: there's only one Pacman in the map.
        if (item == 9): r = r[0]
        return r

    def remove_food(self, loc):
        """Remove the food from a location.\n\n
        Does nothing if specified location does not have food.
        """
        if self[loc] != 1: pass
        else: self[loc] = 0
        
    def move_player(self, loc_old, loc_new):
        """Move the player (Pacman/Ghost) to a new location.\n\n
        Does nothing if specified location does not have Pacman/Ghost.
        """
        if self[loc_old] not in [3, 9]:
            pass
        elif loc_new == loc_old:
            pass
        else:
            self[loc_new] = self[loc_old]
            self[loc_old] = 0
