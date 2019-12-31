import sys # argv
import numpy as np
from collections import deque


with open(sys.argv[1]) as f:
    grid = np.array([list(line[:-1]) for line in f.readlines()])

# make a map of the portals
portals = {}
unpaired_portals = {}
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
                portals[loc] = loc2
                portals[loc2] = loc
            else:
                unpaired_portals[tag] = loc

start_loc = unpaired_portals.pop('AA')
goal_loc = unpaired_portals.pop('ZZ')
assert not unpaired_portals

def get_adjacent_locs(loc: tuple) -> list:
    y, x = loc
    locs = [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]
    if loc in portals:
        locs.append(portals[loc])
    return locs
def bfs(start_loc: tuple, goal_loc: tuple) -> int:
    queue = deque([(start_loc, 0)])
    visited = {start_loc}
    while queue:
        loc, dist = queue.popleft()
        if loc == goal_loc:
            return dist
        for loc2 in get_adjacent_locs(loc):
            if grid[loc2] == '.' and loc2 not in visited:
                visited.add(loc2)
                queue.append((loc2, dist + 1))
    raise RuntimeError("No path found")

print(bfs(start_loc, goal_loc))
