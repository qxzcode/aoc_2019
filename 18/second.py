import sys # argv
import string
from collections import deque
import numpy as np
from heapdict import heapdict


with open(sys.argv[1]) as f:
    grid = []
    object_locs = {}
    loc_objects = {}
    for y,line in enumerate(f):
        grid.append([])
        for x,char in enumerate(line.strip()):
            grid[-1].append(char != '#')
            if char not in '.#':
                loc_objects[(x, y)] = char
                object_locs[char] = (x, y)
grid = np.array(grid).T

# replace the entrance area
start_x, start_y = object_locs['@']
grid[start_x-1:start_x+2, start_y-1:start_y+2] = [
    [True,  False, True ],
    [False, False, False],
    [True,  False, True ],
]
del object_locs['@']
object_locs['1'] = (start_x-1, start_y-1)
object_locs['2'] = (start_x+1, start_y-1)
object_locs['3'] = (start_x-1, start_y+1)
object_locs['4'] = (start_x+1, start_y+1)

# make a more concise graph of shortest paths between keys/doors
def get_adjacent_locs(loc: tuple):
    x, y = loc
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
def find_adjacent_objects(start_loc: tuple):
    queue = deque([(start_loc, 0)])
    visited = {start_loc}
    objects = {}
    while queue:
        loc, dist = queue.popleft()
        for loc2 in get_adjacent_locs(loc):
            if grid[loc2] and loc2 not in visited:
                visited.add(loc2)
                if loc2 in loc_objects:
                    objects[loc_objects[loc2]] = dist+1
                else:
                    queue.append((loc2, dist+1))
    return objects
edges = {
    obj: find_adjacent_objects(loc)
    for obj, loc in object_locs.items()
}

def get_shortest_path_len():
    """Modified Dijkstra's algorithm for collecting all the keys"""
    initial_state = (('1', '2', '3', '4'), frozenset())
    all_keys = frozenset(string.ascii_lowercase) & frozenset(object_locs.keys())
    all_doors = frozenset(string.ascii_uppercase) & frozenset(object_locs.keys())
    
    queue = heapdict()
    queue[initial_state] = 0
    visited = set()
    while queue:
        state, dist = queue.popitem()
        visited.add(state)
        
        nodes, keys = state
        if keys == all_keys:
            return dist
        
        for ni, node in enumerate(nodes):
            for node2, edge_len in edges[node].items():
                if node2 in all_doors and node2.lower() not in keys:
                    continue
                if node2 in all_keys:
                    new_keys = keys | {node2}
                else:
                    new_keys = keys
                new_nodes = nodes[:ni] + (node2,) + nodes[ni+1:]
                new_state = (new_nodes, new_keys)
                if new_state in visited:
                    continue
                new_dist = dist + edge_len
                if new_state not in queue or new_dist < queue[new_state]:
                    queue[new_state] = new_dist
    
    raise RuntimeError("No path found")

print(get_shortest_path_len())
