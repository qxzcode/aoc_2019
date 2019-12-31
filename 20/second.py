import sys # argv
import numpy as np
from collections import deque


with open(sys.argv[1]) as f:
    grid = np.array([list(line[:-1]) for line in f.readlines()])

# make a map of the portals
inner_portals = {}
outer_portals = {}
unpaired_portals = {}
def radius(loc: tuple) -> int:
    y, x = loc
    return max(abs(y - grid.shape[0]//2), abs(x - grid.shape[1]//2))
for (y, x), char in np.ndenumerate(grid):
    if char.isupper():
        tag = None
        if y < grid.shape[0] - 1 and grid[y+1, x].isupper():
            tag = char + grid[y+1, x]
            loc = (y-1, x) if y > 0 and grid[y-1, x] == '.' else (y+2, x)
        elif x < grid.shape[1] - 1 and grid[y, x+1].isupper():
            tag = char + grid[y, x+1]
            loc = (y, x-1) if x > 0 and grid[y, x-1] == '.' else (y, x+2)
        if tag is not None:
            if tag in unpaired_portals:
                loc2 = unpaired_portals.pop(tag)
                if radius(loc) > radius(loc2):
                    loc, loc2 = loc2, loc
                inner_portals[loc] = loc2
                outer_portals[loc2] = loc
            else:
                unpaired_portals[tag] = loc

start_loc = unpaired_portals.pop('AA')
goal_loc = unpaired_portals.pop('ZZ')
assert not unpaired_portals

def get_adjacent_locs(loc: tuple) -> list:
    y, x, d = loc
    locs = [(y+1, x, d), (y-1, x, d), (y, x+1, d), (y, x-1, d)]
    if (y, x) in inner_portals:
        locs.append(inner_portals[(y, x)]+(d+1,))
    if (y, x) in outer_portals and d > 0:
        locs.append(outer_portals[(y, x)]+(d-1,))
    return locs
def bfs(start_loc: tuple, goal_loc: tuple) -> int:
    start_loc += (0,)
    goal_loc += (0,)
    queue = deque([(start_loc, 0)])
    visited = {start_loc}
    while queue:
        loc, dist = queue.popleft()
        if loc == goal_loc:
            return dist
        for loc2 in get_adjacent_locs(loc):
            if grid[loc2[:2]] == '.' and loc2 not in visited:
                visited.add(loc2)
                queue.append((loc2, dist + 1))
    raise RuntimeError("No path found")

print(bfs(start_loc, goal_loc))
