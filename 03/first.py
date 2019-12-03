import sys # argv
import math # inf
from typing import NamedTuple


class Segment(NamedTuple):
    vertical: bool
    pos: int
    min_pos: int
    max_pos: int

def load_segments(input_line: str):
    x1, y1 = 0, 0
    segments = []
    for token in input_line.split(','):
        value = int(token[1:])
        x2, y2, seg = {
            'L': (x1-value, y1, Segment(False, y1, x1-value, x1)),
            'R': (x1+value, y1, Segment(False, y1, x1, x1+value)),
            'U': (x1, y1-value, Segment(True, x1, y1-value, y1)),
            'D': (x1, y1+value, Segment(True, x1, y1, y1+value)),
        }[token[0]]
        segments.append(seg)
        x1, y1 = x2, y2
    return segments

def get_intersection(s1: Segment, s2: Segment):
    if s1.vertical != s2.vertical and s2.min_pos <= s1.pos <= s2.max_pos and s1.min_pos <= s2.pos <= s1.max_pos:
        if s1.vertical:
            return (s2.pos, s1.pos)
        else:
            return (s1.pos, s2.pos)
    return None


# parse the segments from the input file
with open(sys.argv[1]) as f:
    segments1, segments2 = [load_segments(line) for line in f.readlines()]

# find the closest intersection
closest_dist = math.inf
for s1 in segments1:
    for s2 in segments2:
        intersection = get_intersection(s1, s2)
        if intersection is not None:
            x, y = intersection
            dist = abs(x) + abs(y)
            if dist != 0 and dist < closest_dist:
                closest_dist = dist
print(closest_dist)
