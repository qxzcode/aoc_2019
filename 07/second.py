import sys # argv
import math # inf
import itertools # permutations

from typing import Tuple, List, Iterable, Generator


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

def parse_op_value(op_value: int) -> Tuple[int, List[int]]:
    op = op_value % 100
    if op not in OP_NUM_PARAMS:
        raise Exception(f'Invalid op: {op}')
    op_value //= 100
    param_modes = []
    for _ in range(OP_NUM_PARAMS[op]):
        mode = op_value % 10
        assert mode in [0, 1]
        param_modes.append(mode)
        op_value //= 10
    return op, param_modes

def make_program(memory: List[int]) -> Generator[int, int, None]:
    memory = memory.copy()
    
    output_value = None
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
                raise Exception('Attempted to write to immediate parameter')
        
        if op == 1:
            result = get_param(1) + get_param(2)
            set_param(3, result)
        elif op == 2:
            result = get_param(1) * get_param(2)
            set_param(3, result)
        elif op == 3:
            set_param(1, (yield output_value))
            output_value = None
        elif op == 4:
            if output_value is not None:
                raise Exception('Two outputs in a row with no input')
            output_value = get_param(1)
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
    
    if output_value is not None:
        yield output_value


def init_program(phase: int) -> Generator[int, int, None]:
    program = make_program(memory)
    assert program.send(None) is None
    assert program.send(phase) is None
    return program

def run_phase_config(phase_config: Iterable[int]) -> int:
    programs = [init_program(phase) for phase in phase_config]
    output_value = 0
    try:
        while True:
            for program in programs:
                output_value = program.send(output_value)
    except StopIteration:
        return output_value


with open(sys.argv[1]) as f:
    memory = [int(value) for value in f.read().split(',')]

largest_output = -math.inf
largest_output_config = None
for phase_config in itertools.permutations(range(5, 10)):
    output_value = run_phase_config(phase_config)
    if output_value > largest_output:
        largest_output = output_value
        largest_output_config = phase_config
#print(largest_output_config)
print(largest_output)
