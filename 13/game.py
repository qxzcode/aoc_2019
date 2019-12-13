import numpy as np


TILE_STRINGS = {
    0: ' ', # empty
    1: '#', # wall
    2: '=', # block
    3: '-', # horizontal paddle
    4: 'o', # ball
}

class Game:
    def __init__(self, manual=False):
        self.grid = np.zeros((0, 0), dtype=int)
        self.score = None
        self.manual = False
        self._x, self._y = None, None
    
    def input_func(self) -> int:
        if self.manual:
            print()
            self.print_grid()
            print("Score:", self.score)
            return {'a': -1, '': 0, 'd': 1}[input("Move: ").strip()]
        else:
            (ball_y,), (ball_x,) = (self.grid == 4).nonzero()
            (paddle_y,), (paddle_x,) = (self.grid == 3).nonzero()
            return np.sign(ball_x - paddle_x)
    
    def output_func(self, value: int):
        if self._x is None:
            self._x = value
        elif self._y is None:
            self._y = value
        else:
            if self._x == -1 and self._y == 0:
                self.score = value
            else:
                self._set_tile(self._x, self._y, value)
            self._x, self._y = None, None
    
    def _set_tile(self, x: int, y: int, t: int):
        assert t in [0,1,2,3,4], f"Invalid tile value: {t}"
        height, width = self.grid.shape
        if x >= width or y >= height:
            new_grid = np.zeros((max(height, y+1), max(width, x+1)), dtype=int)
            new_grid[:height, :width] = self.grid
            self.grid = new_grid
        self.grid[y, x] = t
    
    def print_grid(self):
        for row in self.grid:
            print(''.join([TILE_STRINGS[t] for t in row]))
