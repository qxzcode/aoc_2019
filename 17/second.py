import sys # argv
from collections import defaultdict

from intcode import load_memory, run_program

class Camera:
    def __init__(self, debug=False):
        self.debug = debug
        
        self.grid = defaultdict(bool)
        self._x = 0
        self._y = 0
        self.width = 0
        self.height = 0
        
        self.start_x = None
        self.start_y = None
        self.start_dir = None
        
        self._got_grid = False
        self._input_buffer = list('A,B,C\nL,3\n3\n3\nn\n')
    
    def input_func(self) -> int:
        char = self._input_buffer.pop(0)
        if self.debug: print(char, end='')
        return ord(char)
    
    def output_func(self, value: int):
        char = chr(value)
        if value < 128:
            if self.debug: print(char, end='')
        else:
            if self.debug: print('\nLarge output value: ', end='')
            print(value)
        
        if self._got_grid:
            pass
        elif char == 'M':
            self._got_grid = True
            self.make_instructions()
        elif char == '\n':
            self._x = 0
            self._y += 1
        else:
            self.grid[(self._x,self._y)] = {
                '.': False, '#': True,
                '^': True, 'V': True, '<': True, '>': True,
                'X': False,
            }[char]
            if char in '^V<>':
                self.start_x = self._x
                self.start_y = self._y
                self.start_dir = {'^': 0, '>': 1, 'V': 2, '<': 3}[char]
            
            self.width = max(self.width, self._x+1)
            self.height = max(self.height, self._y+1)
            self._x += 1
    
    def make_instructions(self):
        # construct the full sequence of moves to be made
        x, y, d = self.start_x, self.start_y, self.start_dir
        full_seq = []
        while True:
            moves = {0: (x,y-1), 1: (x+1,y), 2: (x,y+1), 3: (x-1,y)}
            if self.grid[moves[d]]:
                full_seq.append('-')
                x, y = moves[d]
            elif self.grid[moves[(d+1)%4]]:
                full_seq.append('R')
                d = (d+1)%4
            elif self.grid[moves[(d-1)%4]]:
                full_seq.append('L')
                d = (d-1)%4
            else:
                break
        
        def compress_runs(seq: list) -> list:
            res = []
            run = 0
            for item in seq+['E']:
                if item == '-':
                    run += 1
                else:
                    if run > 0:
                        res.append(str(run))
                        run = 0
                    res.append(item)
            return res[:-1]
        
        full_seq = compress_runs(full_seq)
        
        def make_str(seq: list) -> str:
            s = ''
            run = 0
            for item in seq+['E']:
                if item == '-':
                    run += 1
                else:
                    if run > 0:
                        s += str(run) + ','
                        run = 0
                    if isinstance(item, int):
                        item = f'[{item}]'
                    s += item + ','
            return s[:-3]
        
        def get_next_items(seq: list, func: list) -> set:
            items = []
            for i in range(len(seq) - len(func)):
                if seq[i:i+len(func)] == func:
                    item = seq[i+len(func)]
                    if isinstance(item, str) and item not in items:
                        items.append(item)
            return items
        
        def replace_func(seq: list, func: list, replacement: int) -> list:
            new_seq = []
            i = 0
            while i < len(seq):
                if seq[i:i+len(func)] == func:
                    new_seq.append(replacement)
                    i += len(func)
                else:
                    new_seq.append(seq[i])
                    i += 1
            return new_seq
        
        # main recursive backtracking solver
        def find_solution(seq, funcs):
            # try appending a new item to the current func
            for next_item in get_next_items(seq, funcs[-1]):
                new_func = funcs[-1] + [next_item]
                if len(make_str(new_func)) > 20:
                    continue
                res = find_solution(seq, [*funcs[:-1], new_func])
                if res is not None:
                    return res
            
            # try finishing the current func (if it is non-empty)
            if funcs[-1]:
                new_seq = replace_func(seq, funcs[-1], len(funcs)-1)
                if len(funcs) < 3:
                    res = find_solution(new_seq, funcs+[[]])
                    if res is not None:
                        return res
                else:
                    # verify that the three funcs are a valid solution
                    if all(isinstance(x, int) for x in new_seq):
                        return new_seq, funcs
            
            # no solution was found
            return None
        
        seq, funcs = find_solution(full_seq, [[]])
        final_str = ','.join('ABC'[x] for x in seq)
        final_str += '\n'
        final_str += '\n'.join(make_str(func) for func in funcs)
        final_str += '\nn\n'
        self._input_buffer = list(final_str)
    
    def print_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                char = '#' if self.grid[(x, y)] else '.'
                print(char, end='')
            print()

# run the program
camera = Camera(debug=False)
memory = load_memory(sys.argv[1])
memory[0] = 2
run_program(memory, camera.input_func, camera.output_func)
