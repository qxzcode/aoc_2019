import sys # argv

from robot import Robot
from intcode import load_memory, run_program


robot = Robot()

memory = load_memory(sys.argv[1])
run_program(memory, robot.input_func, robot.output_func)

print(len(robot.grid))
