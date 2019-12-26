import sys # argv

from intcode import load_memory, run_program


input_buffer = []
def input_func() -> int:
    if not input_buffer:
        input_buffer.extend(ord(c) for c in input()+'\n')
    return input_buffer.pop(0)

def output_func(value: int):
    print(chr(value), end='', flush=True)

memory = load_memory(sys.argv[1])
run_program(memory, input_func, output_func)
