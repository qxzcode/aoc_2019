import sys # argv

from intcode import load_memory, run_program

class Camera:
    def __init__(self):
        self.grid = {}
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
    
    def input_func(self) -> int:
        raise NotImplementedError()
    
    def output_func(self, value: int):
        char = chr(value)
        if char == '\n':
            self.x = 0
            self.y += 1
        else:
            self.grid[(self.x,self.y)] = {
                '.': False, '#': True,
                '^': True, 'V': True, '<': True, '>': True,
                'X': False,
            }[char]
            self.width = max(self.width, self.x+1)
            self.height = max(self.height, self.y+1)
            self.x += 1
    
    def print_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                char = '#' if self.grid[(x, y)] else '.'
                print(char, end='')
            print()

# run the program to get the grid
camera = Camera()
memory = load_memory(sys.argv[1])
run_program(memory, camera.input_func, camera.output_func)

# compute the sum of the "alignment parameters"
align_param_sum = 0
for x in range(1, camera.width-1):
    for y in range(1, camera.height-1):
        if all(camera.grid[pos] for pos in [(x,y),(x+1,y),(x-1,y),(x,y+1),(x,y-1)]):
            align_param_sum += x * y
print(align_param_sum)
