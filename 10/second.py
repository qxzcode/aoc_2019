import sys # argv
import numpy as np


# load the grid
with open(sys.argv[1]) as f:
    grid = np.array([[c == '#' for c in line.strip()] for line in f.readlines()])

pivot_y = int(sys.argv[2])
pivot_x = int(sys.argv[3])

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

asteroid_locs = list(zip(*grid.nonzero()))
asteroid_locs.remove((pivot_y, pivot_x))
def destroy_detectable():
    detectable = []
    for y, x in asteroid_locs:
        if not are_occluded(pivot_x, pivot_y, x, y):
            detectable.append([y, x])
    for y, x in detectable:
        grid[y, x] = False
        asteroid_locs.remove((y, x))
    return np.array(detectable)

count = 0
while True:
    detectable = destroy_detectable()
    if count + len(detectable) >= 200:
        break
    count += len(detectable)

angles = np.arctan2(detectable[:,1] - pivot_x, detectable[:,0] - pivot_y)
sort = np.argsort(angles)[::-1]
detectable = detectable[sort]

y, x = detectable[200 - count - 1]
print(x*100 + y)
