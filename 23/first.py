import sys # argv
from typing import List, Optional

from intcode import load_memory, Computer


class NetworkComputer:
    def __init__(self, address: int, memory: List[int]):
        self.address = address
        self.computer = Computer(memory)
        self.input_buffer = [address]
    
    def _input_func(self) -> int:
        if self.input_buffer:
            return self.input_buffer.pop(0)
        else:
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
            x = self._get_next_output()
            y = self._get_next_output()
            send_packet(address, x, y)

memory = load_memory(sys.argv[1])
computers = [NetworkComputer(address, memory) for address in range(50)]

def send_packet(address: int, x: int, y: int):
    if address == 255:
        print(y)
        quit()
    computers[address].input_buffer.extend([x, y])

while True:
    for computer in computers:
        computer.step()
