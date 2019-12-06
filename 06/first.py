import sys # argv
from collections import defaultdict


# load the input file
with open(sys.argv[1]) as f:
    lines = f.readlines()

# build the tree
children_map = defaultdict(list)
parent_map = {}
for line in lines:
    parent, child = line.strip().split(')')
    children_map[parent].append(child)
    parent_map[child] = parent
    if parent not in parent_map:
        parent_map[parent] = None

# find the root
roots = []
for child, parent in parent_map.items():
    if parent is None:
        roots.append(child)
root, = roots

# recurse, counting the total number of orbits
def count_orbits(node: str, depth: int = 0) -> int:
    total_orbits = depth
    for child in children_map[node]:
        total_orbits += count_orbits(child, depth+1)
    return total_orbits
print(count_orbits(root))
