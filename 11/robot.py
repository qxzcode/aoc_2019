class Robot:
    def __init__(self):
        self.grid = {}
        self.is_color_next = True
        self.x = 0
        self.y = 0
        self.direction = 0
    
    def input_func(self) -> int:
        return self.grid.get((self.x, self.y), 0)
    
    def output_func(self, value: int):
        assert value in [0, 1], f"Invalid output value: {value}"
        if self.is_color_next:
            self.grid[(self.x, self.y)] = value
            self.is_color_next = False
        else:
            self.direction += {0: -1, 1: +1}[value]
            self.direction %= 4
            self.x += {0: 0, 1: +1, 2: 0, 3: -1}[self.direction]
            self.y += {0: -1, 1: 0, 2: +1, 3: 0}[self.direction]
            self.is_color_next = True
