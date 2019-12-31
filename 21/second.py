import sys # argv

from intcode import load_memory, run_program


# run the program to get the grid
memory = load_memory(sys.argv[1])

DEBUG = False

# J = (((!B or !C) and D) or !A) and (E or H)
INPUT_STR = """\
NOT B J
NOT C T
OR T J
AND D J
NOT A T
OR T J
OR E T
OR H T
AND T J
RUN
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
