import sys # argv
import re
from typing import Tuple


TOTAL_CARDS = 119315717514047
REPETITIONS = 101741582076661
DESIRED_INDEX = 2020

# compute the linear transformation for the inverse of one shuffle
m = 1
b = 0
with open(sys.argv[1]) as f:
    for line in reversed(list(f)):
        line = line.strip()
        if line == 'deal into new stack':
            # +1
            b += 1
            # *(-1)
            m = -m
            b = -b
        elif match := re.fullmatch(r'cut (-?\d+)', line):
            # +x
            b += int(match[1])
        elif match := re.fullmatch(r'deal with increment (\d+)', line):
            # /x
            inv = pow(int(match[1]), -1, mod=TOTAL_CARDS)
            m *= inv
            b *= inv
        else:
            raise ValueError(f'Invalid line: {line!r}')
        
        # normalize the values to keep them from exploding too much
        m %= TOTAL_CARDS
        b %= TOTAL_CARDS

# repeatedly compose the transformation with itself a la exponentiation-by-squaring
Transform = Tuple[int, int]
def compose(t1: Transform, t2: Transform) -> Transform:
    m1, b1 = t1
    m2, b2 = t2
    return (m2*m1) % TOTAL_CARDS, (m2*b1 + b2) % TOTAL_CARDS  # m2*(m1*x + b1) + b2
def compose_n_times(t: Transform, n: int) -> Transform:
    if n == 1:
        return t
    
    t_squared = compose(t, t)
    if n % 2 == 0:
        return compose_n_times(t_squared, n // 2)
    else:
        return compose(t, compose_n_times(t_squared, n // 2))
m, b = compose_n_times((m, b), REPETITIONS)

# apply the transformation to the desired index
print((m*DESIRED_INDEX + b) % TOTAL_CARDS)
