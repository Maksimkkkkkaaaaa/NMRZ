from src.config import GRID_ROWS, GRID_COLS, SHELVES, ORDERS, PACK_ZONE
from threading import Lock

class Warehouse:
    def __init__(self):
        self.rows = GRID_ROWS
        self.cols = GRID_COLS
        self.grid = [[0] * self.cols for _ in range(self.rows)]

        for (r,c) in SHELVES:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.grid[r][c] = 1

        self.order_positions = set()
        for (r,c) in ORDERS:
            if self.grid[r][c] == 0:
                self.grid[r][c] = 2
                self.order_positions.add((r,c))

        pr, pc = PACK_ZONE
        if self.grid[pr][pc] == 0:
            self.grid[pr][pc] = 3
        self.lock = Lock()

    def is_free(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if self.grid[r][c] == 1:
            return False
        return True

    def has_order(self, r, c):
        with self.lock:
            return (r,c) in self.order_positions

    def pick_order(self, r, c):
        with self.lock:
            if (r,c) in self.order_positions:
                self.order_positions.remove((r,c))
                self.grid[r][c] = 0
                return True
            else:
                return False

    def is_pack_zone(self, r, c):
        return (r, c) == PACK_ZONE
