import sys # argv

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

# count the number of locations affected by the tractor beam
count = 0
for x in range(50):
    for y in range(50):
        if test_location(x, y):
            count += 1
print(count)
