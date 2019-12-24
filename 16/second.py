import sys # argv
import numpy as np


# load the input array
with open(sys.argv[1]) as f:
    arr = np.array([int(d) for d in f.read().strip()])

message_offset = sum(n * 10**i for i, n in enumerate(arr[6::-1]))
total_input_len = len(arr)*10000
assert message_offset >= total_input_len // 2 # for optimization to work

arr = np.tile(arr, 10000)[message_offset:]

# compute the phases
for _ in range(100):
    arr = arr[::-1].cumsum()[::-1] % 10

print(''.join(map(str, arr[:8])))
