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

def get_path_from_root(node: str) -> list:
    path = []
    while True:
        path.append(node)
        node = parent_map[node]
        if node is None:
            path.reverse()
            return path

path1 = get_path_from_root(parent_map['YOU'])
path2 = get_path_from_root(parent_map['SAN'])

# find the point at which the two paths from the root diverge
for i, (n1, n2) in enumerate(zip(path1, path2)):
    if n1 != n2:
        break

print((len(path1) - i) + (len(path2) - i))
