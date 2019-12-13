import sys # argv
import numpy as np
import re


# load the input position data
def parse_position(line):
    m = re.fullmatch(r'<x=([-+\d]+),\s*y=([-+\d]+),\s*z=([-+\d]+)>', line.strip())
    return [int(m[1]), int(m[2]), int(m[3])]
with open(sys.argv[1]) as f:
    positions = np.array([parse_position(line) for line in f])

velocities = np.zeros_like(positions)
num_moons = len(positions)

for _ in range(1000):
    # update velocities (apply gravity)
    for i in range(num_moons):
        for j in range(num_moons):
            velocities[i] += np.sign(positions[j] - positions[i])
    
    # update positions (apply velocities)
    positions += velocities

# calculate and print the total energy
energies = np.abs(positions).sum(axis=-1) * np.abs(velocities).sum(axis=-1)
print(energies.sum())
