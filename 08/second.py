import sys # argv
import numpy as np


# load the input file
with open(sys.argv[1]) as f:
    arr = np.array([int(d) for d in f.read().strip()])

width = int(sys.argv[2])
height = int(sys.argv[3])
arr = arr.reshape(-1, height, width)

first_non2 = np.vectorize(lambda arr: arr[np.where(arr != 2)[0][0]], signature='(n)->()')
image = np.apply_along_axis(first_non2, 0, arr)
for row in image:
    print(''.join(['  ','##'][v] for v in row))
