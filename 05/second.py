import sys # argv


OP_NUM_PARAMS = {
    99: 0,
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
}

def parse_op_value(op_value: int):
    op = op_value % 100
    op_value //= 100
    param_modes = []
    for _ in range(OP_NUM_PARAMS[op]):
        mode = op_value % 10
        assert mode in [0, 1]
        param_modes.append(mode)
        op_value //= 10
    return op, param_modes

def run_program(memory):
    memory = memory.copy()
    
    ip = 0
    while True:
        op, param_modes = parse_op_value(memory[ip])
        if op == 99:
            break
        
        def get_param(n: int) -> int:
            param_value = memory[ip+n]
            if param_modes[n-1] == 0:
                return memory[param_value]
            else:
                return param_value
        
        def set_param(n: int, value: int):
            param_value = memory[ip+n]
            if param_modes[n-1] == 0:
                memory[param_value] = value
            else:
                raise Exception(f'Attempted to write to immediate parameter')
        
        if op == 1:
            result = get_param(1) + get_param(2)
            set_param(3, result)
        elif op == 2:
            result = get_param(1) * get_param(2)
            set_param(3, result)
        elif op == 3:
            set_param(1, int(input('Input: ')))
        elif op == 4:
            print('Output:', get_param(1))
        elif op == 5:
            if get_param(1) != 0:
                ip = get_param(2)
                continue
        elif op == 6:
            if get_param(1) == 0:
                ip = get_param(2)
                continue
        elif op == 7:
            result = get_param(1) < get_param(2)
            set_param(3, int(result))
        elif op == 8:
            result = get_param(1) == get_param(2)
            set_param(3, int(result))
        else:
            raise Exception(f'Invalid op: {op}')
        
        ip += 1 + len(param_modes)
    
    return memory[0]

with open(sys.argv[1]) as f:
    memory = [int(value) for value in f.read().split(',')]
run_program(memory)
