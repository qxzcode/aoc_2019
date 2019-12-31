import sys # argv

from intcode import load_memory, run_program


# run the program to get the grid
memory = load_memory(sys.argv[1])

DEBUG = False

# J = (!C and D) or !A
INPUT_STR = """\
NOT C J
AND D J
NOT A T
OR T J
WALK
"""
input_buffer = [ord(char) for char in INPUT_STR]
def input_func() -> int:
    value = input_buffer.pop(0)
    if DEBUG:
        print(chr(value), end='', flush=True)
    return value

def output_func(value: int):
    if value >= 128:
        print(value)
    elif DEBUG:
        print(chr(value), end='', flush=True)

run_program(memory, input_func, output_func)
