import heapq
import src.map_utils as utils


def backtracking(parents, agent_cord, goal_cord):
    path = [goal_cord]
    while path[-1] != agent_cord:
        path.append(parents[path[-1]])
    path.reverse()
    return path


def manhattan_heuristic_function(agent_cord, goal_cord):
    return abs(agent_cord[0] - goal_cord[0]) + abs(agent_cord[1] - goal_cord[1])


def a_star_search(the_map, agent_cord, goal_cord):
    parents = {}
    explored = []
    frontier = []

    h_start = manhattan_heuristic_function(agent_cord, goal_cord)
    heapq.heappush(frontier, (h_start, (h_start, agent_cord)))

    while True:
        if not frontier:
            return None

        current = heapq.heappop(frontier)

        if current[1][1] in explored:
            continue

        explored.append(current[1][1])

        if current[1][1] == goal_cord:
            for p in parents:
                parents[p] = parents[p][0]
            return backtracking(parents, agent_cord, goal_cord)

        adjacents = utils.remove_object(utils.GetAdjacents(the_map, current[1][1][0], current[1][1][1], True))

        for adj in adjacents:   # adjacents = [(x, y)]
            if adj not in explored:
                current_path_cost = current[0] - manhattan_heuristic_function(current[1][1], goal_cord)
                h_adj = manhattan_heuristic_function(adj, goal_cord)
                adjacent_priority = current_path_cost + 1 + h_adj

                heapq.heappush(frontier, (adjacent_priority, (h_adj, adj)))

                if adj not in parents or parents[adj][1] > adjacent_priority:
                    parents[adj] = [current[1][1], adjacent_priority]


# Unnecessary search
def breadth_first_search(the_map, agent_cord, goal_cord):
    parents = {}
    explored = []
    frontier = [agent_cord]

    while True:
        if not frontier:
            return None

        current = frontier.pop(0)

        if current in explored:
            continue

        explored.append(current)

        if current == goal_cord:
            return backtracking(parents, agent_cord, goal_cord)

        adjacents = utils.GetAdjacents(the_map, current[1][0], current[1][1], True)

        for adj in adjacents:
            if adj not in explored and adj not in frontier:
                frontier.append(adj)
                parents[adj] = current
