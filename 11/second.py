import sys # argv

from robot import Robot
from intcode import load_memory, run_program


robot = Robot()
robot.grid[(0, 0)] = 1

memory = load_memory(sys.argv[1])
run_program(memory, robot.input_func, robot.output_func)

x_coords, y_coords = zip(*robot.grid.keys())
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)

for y in range(y_min, y_max+1):
    for x in range(x_min, x_max+1):
        print({0: '  ', 1: '##'}[robot.grid.get((x, y), 0)], end='')
    print()
