import sys # argv
import numpy as np

from game import Game
from intcode import load_memory, run_program


game = Game()

memory = load_memory(sys.argv[1])
run_program(memory, game.input_func, game.output_func)

print(np.count_nonzero(game.grid == 2))
