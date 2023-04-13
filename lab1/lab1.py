from queue import PriorityQueue
import copy


class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state  # matrix
        self.parent = parent
        self.g = g  # edge cost to reach this node from the start
        # heuristic cost from this node to the goal placement (misplaced tiles or manhattan dist)
        self.h = h

    # Calculates the estimated cost f(n) = g(n) + h(n)
    def f(self):
        return self.g + self.h

    # Less than operator <, returns true or false
    def __lt__(self, other):
        return self.f() < other.f()  # how to prioritize in the frontier list

# Find what index the empty tile has in the matrix


def get_empty_tile(state):
    for row in range(3):
        for col in range(3):
            if state[row][col] == 0:
                return row, col

# Find all neighbors of the empty tile


def get_neighbors(state):
    neighbors = []
    row, col = get_empty_tile(state)  # get index of the empty tile
    if row > 0:
        new_state = copy.deepcopy(state)
        new_state[row][col], new_state[row-1][col] = new_state[row -
                                                               1][col], new_state[row][col]  # swaps the empty tile with the neighbor
        neighbors.append(new_state)  # pushback to array
    if row < 2:
        new_state = copy.deepcopy(state)
        new_state[row][col], new_state[row +
                                       1][col] = new_state[row+1][col], new_state[row][col]
        neighbors.append(new_state)
    if col > 0:
        new_state = copy.deepcopy(state)
        new_state[row][col], new_state[row][col -
                                            1] = new_state[row][col-1], new_state[row][col]
        neighbors.append(new_state)
    if col < 2:
        new_state = copy.deepcopy(state)
        new_state[row][col], new_state[row][col +
                                            1] = new_state[row][col+1], new_state[row][col]
        neighbors.append(new_state)
    return neighbors


def h1(state, goal):
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j] and state[i][j] != 0:
                misplaced_tiles += 1
    return misplaced_tiles


def h2(state, goal):
    manhattan_distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                # quotient and reminder for the state divided by three (for tuple)
                row, col = divmod(state[i][j]-1, 3)
                # manhattan sistance function
                manhattan_distance += abs(row-i) + abs(col-j)
    return manhattan_distance

# A* algorithm for solving the puzzle
# 1. Add root node to frontier list
# 2. Take the first value in fontier list
# 3. Check if state is is goal state
# 4. If not, add the node to explored
# 5. Go through the neighbors for the current state to get the next state

# If goal state
# Add current state to the path and go to its parent
# Add the parent's state to the path
# Lastly, add the start state and then reverse


def a_star(start_state, goal_state, heuristic):
    start_node = Node(start_state, g=0, h=heuristic(start_state, goal_state))
    goal_node = Node(goal_state)
    frontier = PriorityQueue()
    frontier.put(start_node)
    explored = set()

    while not frontier.empty():
        current_node = frontier.get()

        if current_node.state == goal_state:
            path = []
            while current_node.parent is not None:
                # from the goals state add the parents state and so on
                path.append(current_node.state)
                current_node = current_node.parent
            # add start state last, now the path is in backwards order from goal to start
            path.append(start_state)
            path.reverse()  # reverse the array so start is first, goal is last
            return path

        explored.add(tuple(map(tuple, current_node.state)))

        # goes through the neighbors from the zero (empty tile)
        for neighbor_state in get_neighbors(current_node.state):
            # new state after moving the neighbor
            new_state = tuple(map(tuple, neighbor_state))

            if new_state not in explored:   # avoid exploring the same state multiple times
                neighbor_node = Node(neighbor_state, parent=current_node,
                                     g=current_node.g+1, h=heuristic(neighbor_state, goal_state))
                # update frontier list with the neighbor node
                frontier.put(neighbor_node)
    return None


if __name__ == '__main__':
    # start_state = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
    # goal_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

    start_state = [[8, 6, 7], [2, 5, 4], [3, 0, 1]]
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    print('Using h1 heuristic (number of misplaced tiles):')
    path = a_star(start_state, goal_state, h1)
    if path is not None:
        print('Number of moves:', len(path)-1)
        for i, state in enumerate(path):
            print(f'Step {i}:')
            for row in state:
                print(row)
            print()
    else:
        print('No solution found.')

    print('Using h2 heuristic (Manhattan distance):')
    path = a_star(start_state, goal_state, h2)
    if path is not None:
        print('Number of moves:', len(path)-1)
        for i, state in enumerate(path):
            print(f'Step {i}:')
            for row in state:
                print(row)
            print()
    else:
        print('No solution found.')
