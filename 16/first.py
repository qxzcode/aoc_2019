import sys # argv
import numpy as np


# load the input array
with open(sys.argv[1]) as f:
    arr = np.array([int(d) for d in f.read().strip()])
arr_len = len(arr)

# build the transform matrix
fft_matrix = np.empty((arr_len, arr_len), dtype=int)
for i in range(arr_len):
    pattern = np.repeat([0, 1, 0, -1], i+1)
    fft_matrix[i] = np.tile(pattern, arr_len//len(pattern) + 1)[1:arr_len+1]

# compute the phases
for _ in range(100):
    arr = np.abs(fft_matrix @ arr) % 10

print(''.join(map(str, arr[:8])))
