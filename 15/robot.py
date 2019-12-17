class Robot:
    def __init__(self, control_func):
        self.control_func = control_func
        self.grid = {(0, 0): '.'}
        self.last_move = None
        self.x = 0
        self.y = 0
    
    def input_func(self) -> int:
        self.last_move = self.control_func(self.grid, self.x, self.y)
        return self.last_move
    
    def output_func(self, value: int):
        assert value in [0, 1, 2], f"Invalid output value: {value}"
        next_x = self.x + {1: 0, 2: 0, 3: -1, 4: +1}[self.last_move]
        next_y = self.y + {1: -1, 2: +1, 3: 0, 4: 0}[self.last_move]
        self.last_move = None
        if value == 0:
            self.grid[(next_x, next_y)] = '#'
        else:
            self.x = next_x
            self.y = next_y
            char = '.'
            if value == 2:
                char = 'o'
            self.grid[(next_x, next_y)] = char
    
    def print_grid(self):
        x_coords, y_coords = zip(*self.grid.keys())
        x_coords += (self.x,)
        x_coords += (self.y,)
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        for y in range(y_min, y_max+1):
            for x in range(x_min, x_max+1):
                char = self.grid.get((x, y), ' ')
                if x == self.x and y == self.y:
                    char = 'D'
                print(char, end='')
            print()
