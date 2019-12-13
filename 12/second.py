import sys # argv
import numpy as np
import re
import itertools
import math # gcd


def lcm(x, y, z):
    f = math.gcd(math.gcd(x, y), z)
    x //= f
    y //= f
    z //= f
    g = math.gcd(x, y)
    f *= g
    x //= g
    y //= g
    g = math.gcd(x, z)
    f *= g
    x //= g
    z //= g
    g = math.gcd(y, z)
    f *= g
    y //= g
    z //= g
    return f * x * y * z


# load the input position data
def parse_position(line):
    m = re.fullmatch(r'<x=([-+\d]+),\s*y=([-+\d]+),\s*z=([-+\d]+)>', line.strip())
    return [int(m[1]), int(m[2]), int(m[3])]
with open(sys.argv[1]) as f:
    positions = np.array([parse_position(line) for line in f])

velocities = np.zeros_like(positions)
num_moons = len(positions)

def num_iters_until_repeat(positions, velocities):
    x_states = {}
    for iter_num in itertools.count():
        # check if this state has happened before
        x_state = (tuple(positions), tuple(velocities))
        if x_state in x_states:
            assert x_states[x_state] == 0, "the repeated state wasn't the initial state"
            return iter_num
        x_states[x_state] = iter_num
        
        # update velocities (apply gravity)
        velocities += np.sign(np.subtract.outer(positions, positions)).sum(axis=0)
        
        # update positions (apply velocities)
        positions += velocities

x_iters, y_iters, z_iters = [num_iters_until_repeat(positions[:,i], velocities[:,i]) for i in range(3)]
print(lcm(x_iters, y_iters, z_iters))
