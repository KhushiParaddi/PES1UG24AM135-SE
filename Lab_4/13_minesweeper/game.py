from board import Board


class Minesweeper:
    DIFFICULTIES = {
        "easy": (6, 6, 6),
        "medium": (9, 9, 12),
        "hard": (12, 12, 25),
    }

    def __init__(self, difficulty=None):
        if difficulty is None:
            difficulty = self.choose_difficulty()

        difficulty = difficulty.strip().lower()

        if difficulty not in self.DIFFICULTIES:
            raise ValueError(
                "Difficulty must be Easy, Medium, or Hard."
            )

        rows, cols, mines = self.DIFFICULTIES[difficulty]
        self.difficulty = difficulty
        self.board = Board(rows=rows, cols=cols, mines=mines)

    @classmethod
    def choose_difficulty(cls):
        while True:
            print("Choose difficulty: Easy, Medium, or Hard")
            choice = input("Difficulty: ").strip().lower()

            if choice in cls.DIFFICULTIES:
                return choice

            print("Invalid difficulty. Enter Easy, Medium, or Hard.")

    def display(self, reveal_mines=False):
        b = self.board
        print("\n   " + " ".join(str(c + 1) for c in range(b.cols)))
        for r in range(b.rows):
            cells = []
            for c in range(b.cols):
                pos = (r, c)
                if reveal_mines and pos in b.mines:
                    ch = "*"
                elif pos in b.flags:
                    ch = "F"
                elif pos not in b.revealed:
                    ch = "#"
                elif pos in b.mines:
                    ch = "*"
                else:
                    ch = str(b.adjacent_mines(r, c))
                cells.append(ch)
            print(f"{r + 1:2} " + " ".join(cells))

    def run(self):
        print("Minesweeper")
        print("Commands: r row col | f row col | q")
        while True:
            self.display()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            parts = raw.split()
            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Use r row col or f row col.")
                continue
            try:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not self.board.in_bounds(r, c):
                print("Outside the board.")
                continue

            pos = (r, c)

            if parts[0] == "f":
                self.board.toggle_flag(pos)
                continue

            # Give feedback for ignored reveals without changing board state.
            if pos in self.board.flags:
                print("Cell is flagged. Unflag it before revealing.")
                continue
            if pos in self.board.revealed:
                print("Cell already revealed.")
                continue

            revealed_before = len(self.board.revealed)
            adjacent = self.board.adjacent_mines(r, c)
            hit_mine = self.board.reveal(pos)
            revealed_after = len(self.board.revealed)

            if hit_mine:
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine.")
                return

            if self.board.won():
                self.display()
                print("You cleared the board!")
                return

            if adjacent == 0:
                expanded = revealed_after - revealed_before
                if expanded > 1:
                    print(
                        f"Empty cell revealed. Flood-fill expanded "
                        f"to {expanded} cells."
                    )
                else:
                    print("Empty cell revealed. Adjacent mines: 0.")
            else:
                print(f"Safe cell revealed. Adjacent mines: {adjacent}.")
