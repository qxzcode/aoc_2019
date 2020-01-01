import sys # argv
import numpy as np


# load the initial grid
with open(sys.argv[1]) as f:
    grid = [[{'.': 0, '#': 1}[c] for c in line.strip()] for line in f]
grid = np.array(grid)
grid_tmp = np.empty_like(grid)

tile_ratings = 2 ** np.arange(grid.size).reshape(grid.shape)

past_ratings = set()
while True:
    rating = np.einsum('ij,ij', grid, tile_ratings)
    if rating in past_ratings:
        print(rating)
        break
    past_ratings.add(rating)
    
    # compute the next iteration
    for (y, x), t in np.ndenumerate(grid):
        count = 0
        if x > 0: count += grid[y, x-1]
        if x < grid.shape[1]-1: count += grid[y, x+1]
        if y > 0: count += grid[y-1, x]
        if y < grid.shape[1]-1: count += grid[y+1, x]
        grid_tmp[y, x] = count == 1 or (count == 2 and not t)
    grid, grid_tmp = grid_tmp, grid
