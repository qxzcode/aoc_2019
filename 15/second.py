import sys # argv

from robot import Robot
from intcode import load_memory, run_program


# unused; for testing
def manual(grid, rx, ry):
    return {'w': 1, 's': 2, 'a': 3, 'd': 4}[input("Move: ")]

def explore(grid, rx, ry):
    # perform a breadth-first search to find the closest reachable unexplored tile
    queue = [(rx, ry)]
    visited = {(rx, ry): None}
    while queue:
        x, y = queue.pop(0)
        move_dir = visited[(x, y)]
        for x2, y2, d in [(x+1,y,4),(x-1,y,3),(x,y+1,2),(x,y-1,1)]:
            res = d if move_dir is None else move_dir
            if (x2, y2) in visited:
                continue
            if (x2, y2) not in grid:
                return res
            elif grid[(x2,y2)] != '#':
                queue.append((x2, y2))
            visited[(x2, y2)] = res
    raise RuntimeError('Everything explored')

robot = Robot(explore)

memory = load_memory(sys.argv[1])
try:
    run_program(memory, robot.input_func, robot.output_func)
except RuntimeError:
    pass

# perform a breadth-first search to find the O2 system
def get_O2_location(grid):
    queue = [(0, 0)]
    visited = {(0, 0): 0}
    while queue:
        x, y = queue.pop(0)
        distance = visited[(x, y)] + 1
        for x2, y2, d in [(x+1,y,4),(x-1,y,3),(x,y+1,2),(x,y-1,1)]:
            if (x2, y2) in visited:
                continue
            char = grid[(x2,y2)]
            if char == 'o':
                return (x2, y2)
            elif char != '#':
                queue.append((x2, y2))
            visited[(x2, y2)] = distance
    raise RuntimeError("Didn't find the oxygen system")

# perform a breadth-first search to count how far away the farthest space is
def get_max_dist(grid, start_x, start_y):
    next_tiles = [(start_x, start_y)]
    visited = {(start_x, start_y)}
    distance = -1
    while next_tiles:
        distance += 1
        current_tiles = next_tiles
        next_tiles = []
        for x, y in current_tiles:
            for x2, y2 in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
                if (x2, y2) in visited:
                    continue
                if grid[(x2,y2)] != '#':
                    next_tiles.append((x2, y2))
                visited.add((x2, y2))
    return distance

o2_x, o2_y = get_O2_location(robot.grid)
print(get_max_dist(robot.grid, o2_x, o2_y))
