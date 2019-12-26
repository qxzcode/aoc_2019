import sys # argv
import itertools

from intcode import load_memory, run_program


input_buffer = []
def queue_string(input_str: str):
    input_buffer.extend(ord(c) for c in input_str)

queue_string("""north
take mutex
east
east
east
take whirled peas
west
west
west
south
west
take space law space brochure
north
take loom
south
south
take hologram
west
take manifold
east
north
east
south
take cake
west
south
take easter egg
south
""")

items = [
    'mutex',
    'whirled peas',
    'space law space brochure',
    'loom',
    'hologram',
    'manifold',
    'cake',
    'easter egg',
]
for item in items:
    queue_string(f'drop {item}\n')
for config in itertools.product([True,False], repeat=len(items)):
    for take, item in zip(config, items):
        if take:
            queue_string(f'take {item}\n')
    queue_string('south\n')
    for take, item in zip(config, items):
        if take:
            queue_string(f'drop {item}\n')

def input_func() -> int:
    if not input_buffer:
        input_buffer.extend(ord(c) for c in input()+'\n')
    return input_buffer.pop(0)

def output_func(value: int):
    print(chr(value), end='', flush=True)

memory = load_memory(sys.argv[1])
run_program(memory, input_func, output_func)
