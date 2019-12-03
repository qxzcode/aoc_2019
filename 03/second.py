import sys # argv
import math # inf
from typing import NamedTuple


class Segment(NamedTuple):
    vertical: bool
    positive: bool
    base_steps: int
    pos: int
    min_pos: int
    max_pos: int

def load_segments(input_line: str):
    x1, y1 = 0, 0
    steps = 0
    segments = []
    for token in input_line.split(','):
        value = int(token[1:])
        x2, y2, seg = {
            'L': (x1-value, y1, Segment(False, False, steps, y1, x1-value, x1)),
            'R': (x1+value, y1, Segment(False, True, steps, y1, x1, x1+value)),
            'U': (x1, y1-value, Segment(True, False, steps, x1, y1-value, y1)),
            'D': (x1, y1+value, Segment(True, True, steps, x1, y1, y1+value)),
        }[token[0]]
        segments.append(seg)
        x1, y1 = x2, y2
        steps += value
    return segments

def get_intersection_steps(s1: Segment, s2: Segment) -> int:
    def get_seg_steps(s1: Segment, s2: Segment) -> int:
        if s1.positive:
            return s1.base_steps + (s2.pos - s1.min_pos)
        else:
            return s1.base_steps + (s1.max_pos - s2.pos)
    
    if s1.vertical != s2.vertical and s2.min_pos <= s1.pos <= s2.max_pos and s1.min_pos <= s2.pos <= s1.max_pos:
        return get_seg_steps(s1, s2) + get_seg_steps(s2, s1)
    return None


# parse the segments from the input file
with open(sys.argv[1]) as f:
    segments1, segments2 = [load_segments(line) for line in f.readlines()]

# find the closest intersection
min_steps = math.inf
for s1 in segments1:
    for s2 in segments2:
        steps = get_intersection_steps(s1, s2)
        if steps is not None and steps != 0 and steps < min_steps:
            min_steps = steps
print(min_steps)
