import sys # argv
import itertools

from intcode import load_memory, run_program


# run the program to get the grid
memory = load_memory(sys.argv[1])

def test_location(x: int, y: int) -> bool:
    input_buffer = [x, y]
    def input_func() -> int:
        return input_buffer.pop(0)
    
    output_buffer = []
    def output_func(value: int):
        output_buffer.append(value)
    
    run_program(memory, input_func, output_func)
    output_value, = output_buffer
    return {0: False, 1: True}[output_value]

def find_start_loc() -> tuple:
    for dist in itertools.count(start=1):
        for x in range(dist):
            if test_location(x, dist):
                return x, dist
        for y in range(dist+1):
            if test_location(dist, y):
                return dist, y

start_x, start_y = find_start_loc()
x = start_x
min_y = start_y
max_y = start_y
max_y_history = []
while True:
    while not test_location(x, min_y):
        min_y += 1
    while test_location(x, max_y):
        max_y += 1
    max_y_history.append(max_y)
    if len(max_y_history) >= 100 and max_y_history[-100] - min_y >= 100:
        print((x-100+1)*10000 + min_y)
        break
    x += 1
