import sys # argv
import numpy as np


# load the grid
with open(sys.argv[1]) as f:
    grid = np.array([[c == '#' for c in line.strip()] for line in f.readlines()])

def are_occluded(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    g = np.gcd(dx, dy)
    dx //= g
    dy //= g
    for n in range(1, g):
        if grid[y1 + dy*n, x1 + dx*n]:
            return True
    return False

total_asteroids = np.count_nonzero(grid)
counts = np.zeros(total_asteroids, dtype=int)

asteroid_locs = list(zip(*grid.nonzero()))
for i1, (y1, x1) in enumerate(asteroid_locs):
    for i2, (y2, x2) in enumerate(asteroid_locs):
        if i1 != i2 and not are_occluded(x1, y1, x2, y2):
            counts[i1] += 1

print("Max count:", counts.max())
print("Location:", asteroid_locs[np.argmax(counts)])
