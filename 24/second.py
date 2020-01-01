import sys # argv
import numpy as np


# load the initial grid
with open(sys.argv[1]) as f:
    grid = [[{'.': False, '#': True}[c] for c in line.strip()] for line in f]
grid = np.array([grid])

for _ in range(200):
    # compute the next iteration
    grid_tmp = np.zeros((grid.shape[0]+2,)+grid.shape[1:], dtype=bool)
    for d, y, x in np.ndindex(grid_tmp.shape):
        if x == 2 and y == 2:
            continue
        
        count = 0
        
        if d >= 1:
            if x > 0:
                if d <= grid.shape[0]:
                    count += grid[d-1, y, x-1]
            elif d >= 2:
                count += grid[d-2, 2, 1]
            
            if x < 4:
                if d <= grid.shape[0]:
                    count += grid[d-1, y, x+1]
            elif d >= 2:
                count += grid[d-2, 2, 3]
            
            if y > 0:
                if d <= grid.shape[0]:
                    count += grid[d-1, y-1, x]
            elif d >= 2:
                count += grid[d-2, 1, 2]
            
            if y < 4:
                if d <= grid.shape[0]:
                    count += grid[d-1, y+1, x]
            elif d >= 2:
                count += grid[d-2, 3, 2]
        
        if d < grid.shape[0]:
            if y == 1 and x == 2:
                count += np.count_nonzero(grid[d, 0, :])
            elif y == 3 and x == 2:
                count += np.count_nonzero(grid[d, 4, :])
            elif y == 2 and x == 1:
                count += np.count_nonzero(grid[d, :, 0])
            elif y == 2 and x == 3:
                count += np.count_nonzero(grid[d, :, 4])
        
        t = (1 <= d <= grid.shape[0]) and grid[d-1, y, x]
        grid_tmp[d, y, x] = count == 1 or (count == 2 and not t)
    
    grid = grid_tmp
    while not np.any(grid[0]):
        grid = grid[1:]
    while not np.any(grid[-1]):
        grid = grid[:-1]

print(np.count_nonzero(grid))
