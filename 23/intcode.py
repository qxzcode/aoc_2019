from typing import List, Callable, Optional


_OP_NUM_PARAMS = {
    99: 0,
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 1,
}

def _parse_op_value(op_value: int):
    op = op_value % 100
    if op not in _OP_NUM_PARAMS:
        raise Exception(f'Invalid op: {op}')
    op_value //= 100
    param_modes = []
    for _ in range(_OP_NUM_PARAMS[op]):
        mode = op_value % 10
        assert mode in [0, 1, 2], f'Invalid param mode: {mode}'
        param_modes.append(mode)
        op_value //= 10
    return op, param_modes


class Computer:
    def __init__(self, memory: List[int]):
        self.memory = memory.copy()
        self.ip = 0  # instruction pointer
        self.rb = 0  # relative base
    
    def step(self, input_func: Callable[[], int]) -> Optional[int]:
        op, param_modes = _parse_op_value(self.memory[self.ip])
        if op == 99:
            raise RuntimeError('Intcode program halted')
        
        def extend_memory(pos: int):
            if pos >= len(self.memory):
                self.memory.extend([0]*(pos - len(self.memory) + 1))
        
        def get_param_address(param_value: int, param_mode: int) -> Optional[int]:
            if param_mode == 1:
                return None
            if param_mode == 2:
                param_value += self.rb
            extend_memory(param_value)
            return param_value
        
        def get_param(n: int) -> int:
            param_value = self.memory[self.ip+n]
            param_address = get_param_address(param_value, param_modes[n-1])
            if param_address is not None:
                return self.memory[param_address]
            else:
                return param_value
        
        def set_param(n: int, value: int):
            param_value = self.memory[self.ip+n]
            param_address = get_param_address(param_value, param_modes[n-1])
            if param_address is not None:
                self.memory[param_address] = value
            else:
                raise Exception('Attempted to write to immediate parameter')
        
        output_value = None
        if op == 1:
            result = get_param(1) + get_param(2)
            set_param(3, result)
        elif op == 2:
            result = get_param(1) * get_param(2)
            set_param(3, result)
        elif op == 3:
            set_param(1, input_func())
        elif op == 4:
            output_value = get_param(1)
        elif op == 5:
            if get_param(1) != 0:
                self.ip = get_param(2)
                return None
        elif op == 6:
            if get_param(1) == 0:
                self.ip = get_param(2)
                return None
        elif op == 7:
            result = get_param(1) < get_param(2)
            set_param(3, int(result))
        elif op == 8:
            result = get_param(1) == get_param(2)
            set_param(3, int(result))
        elif op == 9:
            self.rb += get_param(1)
        else:
            raise Exception(f'Invalid op: {op}')
        
        self.ip += 1 + len(param_modes)
        return output_value


def load_memory(filename: str) -> List[int]:
    with open(filename) as f:
        return [int(value) for value in f.read().split(',')]
