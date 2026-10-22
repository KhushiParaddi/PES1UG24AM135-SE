
import random

DEFAULT_ROWS = 6
DEFAULT_COLS = 6
DEFAULT_MINES = 6


class Board:
    def __init__(self, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, mines=DEFAULT_MINES):
        if rows < 1 or cols < 1:
            raise ValueError("Rows and columns must be positive.")
        if not 0 <= mines < rows * cols:
            raise ValueError("Mine count must be non-negative and less than total cells.")

        self.rows = rows
        self.cols = cols
        self.mine_total = mines
        self.mines = self._build_mines()
        self.revealed = set()
        self.flags = set()

    
    def __init__(self, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, mines=DEFAULT_MINES):
        if not isinstance(rows, int) or isinstance(rows, bool) or rows <= 0:
            raise ValueError("Rows must be a positive integer.")

        if not isinstance(cols, int) or isinstance(cols, bool) or cols <= 0:
            raise ValueError("Columns must be a positive integer.")

        if not isinstance(mines, int) or isinstance(mines, bool):
            raise ValueError("Mine count must be an integer.")

        if mines < 0 or mines >= rows * cols:
            raise ValueError("Mine count must be non-negative and less than the board size.")

        self.rows = rows
        self.cols = cols
        self.mine_total = mines
        self.mines = self._build_mines()
        self.revealed = set()
        self.flags = set()

    def _build_mines(self):
        cells = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
        ]
        return set(random.sample(cells, self.mine_total))

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        if not self.in_bounds(r, c):
            return

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, c + dc

                if self.in_bounds(nr, nc):
                    yield nr, nc

    def adjacent_mines(self, r, c):
        if not self.in_bounds(r, c):
            return 0

        return sum(
            pos in self.mines
            for pos in self.neighbors(r, c)
        )

    def reveal(self, start):
        r, c = start

        if not self.in_bounds(r, c):
            return False

        if start in self.flags or start in self.revealed:
            return False

        stack = [start]
        hit_mine = False

        while stack:
            pos = stack.pop()

            if not self.in_bounds(*pos):
                continue

            if pos in self.revealed or pos in self.flags:
                continue

            r, c = pos
            self.revealed.add(pos)

            if pos in self.mines:
                hit_mine = True
                continue

            if self.adjacent_mines(r, c) == 0:
                stack.extend(
                    n for n in self.neighbors(r, c)
                    if n not in self.revealed and n not in self.flags
                )

        return hit_mine
    def toggle_flag(self, pos):
  
        r, c = pos

        if not self.in_bounds(r, c):
            return False

        if pos in self.revealed:
           return False

        if pos in self.flags:
            self.flags.remove(pos)
        else:
            self.flags.add(pos)

        return True


    def won(self):
        return all(
            (r, c) in self.revealed
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in self.mines
    )

