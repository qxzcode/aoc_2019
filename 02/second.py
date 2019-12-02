import sys # argv


def run_program(memory, noun, verb):
    memory = list(memory) # make a copy before modifying it
    memory[1] = noun
    memory[2] = verb
    
    ip = 0
    while True:
        op = memory[ip]
        if op == 99:
            break
        value1 = memory[memory[ip+1]]
        value2 = memory[memory[ip+2]]
        if op == 1:
            result = value1 + value2
        elif op == 2:
            result = value1 * value2
        else:
            raise Exception(f'Invalid op: {op}')
        memory[memory[ip+3]] = result
        ip += 4
    
    return memory[0]

with open(sys.argv[1]) as f:
    memory = [int(value) for value in f.read().split(',')]

TARGET_OUTPUT = int(sys.argv[2])
for noun in range(100):
    for verb in range(100):
        if run_program(memory, noun, verb) == TARGET_OUTPUT:
            print(100*noun + verb)
