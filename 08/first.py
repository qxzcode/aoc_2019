import sys # argv
import numpy as np


# load the input file
with open(sys.argv[1]) as f:
    arr = np.array([int(d) for d in f.read().strip()])

width = int(sys.argv[2])
height = int(sys.argv[3])
arr = arr.reshape(-1, height, width)

fewest_zeros_layer = np.argmax(np.count_nonzero(arr, axis=(1, 2)))
digit_counts = np.bincount(arr[fewest_zeros_layer].ravel())
print(digit_counts[1] * digit_counts[2])
