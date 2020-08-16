# AI - Project 01 "Pacman"
- Project for course **CSC14003 @ 18CLC6** "Introduction to Artificial Intelligence"
- Group includes **3 members**:
    - `18127080`: Kiều Vũ Minh Đức ([@kvmduc](https://github.com/kvmduc))
    - `18127185`: Bùi Vũ Hiếu Phụng ([@alecmatts](https://github.com/alecmatts))
    - `18127221`: Bùi Văn Thiện ([@84436](https://github.com/84436))
- **Assignment plan**:
    - Phụng: Level 1/2, 3
    - Đức: Level 3, 4
    - Thiện: Map and PyGame
- **Software stack** used in this project:
    - Language: Python3
    - Libraries (**Dependencies**): PyGame (for map visualization)
    - IDE: PyCharm Community Edition, JupyterLab, VSCode
- **Progress** (on the scale of `1.00`):
    - `0.80` Basis (map, player, search)
    - `1.00` PyGame
    - `1.00` Level 1
    - `1.00` Level 2
    - `0.80` Level 3
    - `0.20` Level 4 (incomplete implementation)



# Quick start

- Install PyGame
- (Optional) Place other (correctly formatted) maps into `./maps`
- Run `src/main.py`
    - Arguments (in exact order): `[level number: 1-3] [mapfile (without extensions)]`
    - By default, `level number` is set to `3` and `mapfile` to `macpan`
- Press `[> Step 1]` to manually step through the process, or `[>>> Step all]` to autorun.
    Keep an eye on messages in console as well.



---



# Structure

This program includes a core module named `pacman` and `main.py` containing GUI code. The core revolves around the **Map** – **Players** (agents) – **Levels** (level solvers) model.



### `map_utils.py`: Map Class

- This class provides containers for maps and basic operations for working with them, including:
    - A map parser: `parse_file()`
    - Searching methods:
        - `get_items()` for fetching item coordinate lists;
        - `get_adjacents()` for getting (maximum) nearest 4 possible tile to move for players;
        - `get_map_slice()` for temporarily limiting visibility for Pacman (required in Level 3)
    - Manipulation methods:
        - `remove_food()` for removing food at specified tile (if applicable)
        - `move_player()` for moving player from one tile to another (if applicable)
- The map is stored as a simple 2D array.



### `search.py`: Search algorithms

- This submobule provides searching algorithms used by agents, which is primarily A* with Manhattan distance heuristic.
- Implementation method:
    - A priority queue is used as the frontier of algorithm, with the priority value as the evaluation of $f(n) = g(n) + h(n)$ in A*, or, in other words, sum of the current total state cost and heuristic evaluation.
    - For heuristics, Manhattan distance is chosen since it is a known admissible heuristic. It can be calculated simply by summing up the differences between coordinates of player and its target on the map.
- A* is chosen as the main search algorithm for the following reasons:
    - A* is more optimal than other uninformed search algorithms (depth-first/breadth-first, uniform-cost, etc.), given that the heuristics used is _admissible_ (i.e. it never overshoots the actual path cost).
    - A* time and space complexity is less than BFS - another algorithm will return an optimal solution but with expensive space complexity  since it will expand all posible successor from a state, since it just expand the node with minimal evaluation value $f(n)$.
        - Sidenote: UCS is also an optimal search algorithm, it is an special case of A* algorithm with heuristic funtion is $h(n) = 0$.



### `player.py`: Players

- This class provides implementation for Pacman and Ghosts
- The players remember their current positions and their target paths, which usually points to their corresponding targets -- food for Pacman and Pacman himself for Ghosts. Additionally, Pacman, a subclass derived from Player, also keeps track of his score.
    - The rules of the score are: `-1` for every step moved, `+20` for every food eaten.
- The players have many methods for searching adapted to each specific levels. However, they **do not** actively "take turn and make their moves": they only return the next move (and other relevant info, if needed) to level solvers, so that level solvers may actually move them on the map.



### `level*.py`: Level solvers

- There are 2 solvers corresponding to 3 levels: Level 1/2 and Level 3
    - Currently implementation for Level 4 is **not completed**, hence there having 3 levels available for running.
    - Level 1 and 2 are considered to be nearly identical, since ghost(s) in Level 2 do not move, thus Pacman can regard them as nothing more than walls/obstacles
- A level is defined as a complete game containing objects which exist based on project description: `1` map, `1` Pacman, `0+` Ghost, and `1+` Food.
- Each level solver takes in a map, generates and initializes Pacman (and Ghosts, if any exists)
- Each level has a method for taking a "step", that is, to allow every players to make their move and update the map as needed on a turn-based basis.
    - This design decision was made to ease implementation of the GUI based on PyGame: since PyGame is required to cotinuously process events (I/O, display, etc.), moving the program main control flow from the level solvers to PyGame (and make the solvers be able to run on a per-turn/on-request basis) eliminates the PyGame hanging in the background (and consequently crashing on itself, if the time between each turn is long enough) and requiring workarounds (moving PyGame to a separate thread, for example)
- In this project, we choose to maximize number of foods eaten instead of maximizing score so that the algorithm can run freely without being constrained with path length



---



# Levels

### Level 1 + 2
- Solver of level 1 and 2 is combined into one because the only difference is the appearance of `Ghost` but at this level, `Ghosts` are unable to move so `Pacman` will see them as walls. Because of that reason, `turn_queue` will not include `Ghost`
- Map at this level only have one food and no other threat so we only need to search once
- With each move, `pop()` next position from the path to target saved in `Player` and update its position in map. Also keep track of game state (finish or not)

##### Comments
- Simple map, simple request. Pacman can easily solve every case. 
- If there is no path, game ends.



### Level 3
- Initially, we discussed to use DFS, we can keep track of node that have explore, according to max size, `Pacman` will know where to go. But we found some obstacles that make we ambigous to solve:
    + What happen if a `Pacman` encounter with a `Ghost` and what is the right behavior of `Pacman`
    At the following example, `Pacman` encounter a `Ghost`, `Pacman` do not know the initial coordinate of `Ghost`, so we plan to segment the area that `Ghost` can reach, figure out, it's large (5x5). Hence, we didn't follow this plan.
    + What if `Pacman` can't explore all map
    ![](https://i.imgur.com/tMNdh3m.png)
    ```
    Yellow square represent for Pacman coordinate
    Green square represent for Food coordinate
    Red zone represent for area that Ghost can reach
    The symbol on Red zone represent for Ghost current coordinate
    ```
    For example in this situation, `Pacman` can't explore whole map, it have two option : end game or try to sneak through. So far, my team project's structure has been build following coordinate, so it means we can't skip the action to learn the pattern of `Ghost` moving.
- So it lead us to another method, which is randomly move until `Pacman` found a food and `Pacman` will keep distance from `Ghost` 2 unit.
- Because of ambitious project description, we do not know if `Pacman` can scan rhombus or square, so we choose it to be a 7x7 square around the `Pacman`
- `Ghost` moves are limited: only move  move one step in any valid direction (if any) around the initial location at the start of the game and completely random
- As `Pacman` is blind, its vision will be updated every move. The solver has this current solution:
    - At that position, search to every food in the vision and follow the closest food and will follow that food until it is eaten.
        - In case `Ghost` is at the next move, delete the current path and re-search (hill-climbing)
    - If there is no food in sight, or no path to any food, pick a random move which is not adjacent to any `Ghost` to prevent the case that at next turn, `Ghost` can kill `Pacman` 
    - Because the path is construct on the child map which is sliced from the original map, we have to generate the direction of that move and convert it to real move in original map

##### Comments
- Cost of random move is very big. If lucky, `Pacman` will randomly move to the sight which contains foods. Otherwise, it will continuously take an fuzzy action.
- To prevent non-stop `Pacman`, we define a variable `max_iter` in level 3. If we pass `max_iter` turn, no wonder `Pacman` has eaten all foods or not, the game ends



### Level 4
At level 4, we plan to use Minimax algorithm to solve the adversarial search, we implemented the Minimax, but it lead to a problem, that is `Pacman` stuck in the infinite loop of current state, which means `Pacman` can explore further than 3 step. With some few remaining time, we can't find the real the problem is. So we skipped this Level 



---



# References
- [GitHub: `brunofalmeida/Pacman-Pygame`](https://github.com/brunofalmeida/Pacman-Pygame): inspiration for PyGame main event loop and skeleton
- [PyGame documentations](https://www.pygame.org/docs/)
- [StackOverflow: "PyGame button single click"](https://stackoverflow.com/a/47664205): inspiration for current implementation of buttons in PyGame GUI
- [Stanford CS221 Project](https://stanford.edu/~cpiech/cs221/homework/prog/pacman/pacman.html) : Approach to project