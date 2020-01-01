import sys # argv
from typing import List, Optional

from intcode import load_memory, Computer


class NetworkComputer:
    def __init__(self, address: int, memory: List[int]):
        self.address = address
        self.computer = Computer(memory)
        self.input_buffer = [address]
        self.read_fail_count = 0
    
    def _input_func(self) -> int:
        if self.input_buffer:
            self.read_fail_count = 0
            return self.input_buffer.pop(0)
        else:
            self.read_fail_count += 1
            return -1
    
    def _step_computer(self) -> Optional[int]:
        return self.computer.step(self._input_func)
    
    def _get_next_output(self) -> int:
        while (output := self._step_computer()) is None:
            pass
        return output
    
    def step(self):
        address = self._step_computer()
        if address is not None:
            self.read_fail_count = 0
            x = self._get_next_output()
            y = self._get_next_output()
            send_packet(address, x, y)
    
    def is_idle(self) -> bool:
        return self.read_fail_count >= 2 and not self.input_buffer

memory = load_memory(sys.argv[1])
computers = [NetworkComputer(address, memory) for address in range(50)]

nat_x, nat_y = None, None
def send_packet(address: int, x: int, y: int):
    if address == 255:
        global nat_x, nat_y
        nat_x, nat_y = x, y
    else:
        computers[address].input_buffer.extend([x, y])

last_nat_y = None
while True:
    is_idle = True
    for computer in computers:
        if not computer.is_idle():
            is_idle = False
            computer.step()
    if is_idle:
        if nat_y == last_nat_y:
            print(nat_y)
            quit()
        last_nat_y = nat_y
        send_packet(0, nat_x, nat_y)
