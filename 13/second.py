import sys # argv

from game import Game
from intcode import load_memory, run_program


game = Game()

memory = load_memory(sys.argv[1])
memory[0] = 2
run_program(memory, game.input_func, game.output_func)

print("Final score:", game.score)
