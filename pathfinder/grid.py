# pathfinder/grid.py
from .constants import ROWS, COLS

class Grid:
    """Represents the grid, handling walls, start/end points, and neighbors."""
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.start = (0, 0)
        self.end = (self.rows - 1, self.cols - 1)
        self.walls = set()

    def in_bounds(self, r, c):
        """Checks if a cell (r, c) is within the grid boundaries."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        """Yields valid neighbors for a given cell."""
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and (nr, nc) not in self.walls:
                yield (nr, nc)

def manhattan_distance(a, b):
    """Calculates the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
