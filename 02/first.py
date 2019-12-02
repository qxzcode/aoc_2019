import sys # argv


with open(sys.argv[1]) as f:
    memory = [int(value) for value in f.read().split(',')]
    memory[1] = 12
    memory[2] = 2
    
    pc = 0
    while True:
        op = memory[pc]
        if op == 99:
            break
        value1 = memory[memory[pc+1]]
        value2 = memory[memory[pc+2]]
        if op == 1:
            result = value1 + value2
        elif op == 2:
            result = value1 * value2
        else:
            raise Exception(f'Invalid op: {op}')
        memory[memory[pc+3]] = result
        pc += 4
    
    print(memory[0])
