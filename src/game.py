from itertools import groupby


class NonoGame:

    # dunder: double under
    def __init__(self, filepath=None, constaints=None):
        # r - read (default)
        # w - write
        if filepath is None and constaints is None:
            raise ValueError("At least one of filepath and constaints must be provided")
        if filepath is not None:
            self.row_constraints = []
            self.col_constraints = []
            # ~= fin = open(filepath)
            with open(filepath) as fin:
                n, m = map(int, fin.readline().strip().split())
                self.n, self.m = n, m
                # Row contraints
                for _ in range(n):
                    tmp = list(map(int, fin.readline().strip().split()))
                    self.row_constraints.append(tmp)
                # Column contraints
                for _ in range(m):
                    tmp = list(map(int, fin.readline().strip().split()))
                    self.col_constraints.append(tmp)
        else:
            self.row_constraints = constaints[0]
            self.col_constraints = constaints[1]

        self.puzzle = [['?' for _ in range(m)] for _ in range(n)]
        self.completed = True
        self.correct = False
        # self.n, self.m = 5, 5

    def print(self):
        COL_LENGTH = 15
        ROW_LENGTH = 15

        # Display Column constraints
        col_display_begin = COL_LENGTH
        column_display = [[' ' for _ in range(self.m)]
                          for _ in range(COL_LENGTH)]
        for col_idx, col_constraint in enumerate(self.col_constraints):
            col_constraint_str = ' '.join(map(str, col_constraint[::-1]))
            for row_idx, ch in zip(range(COL_LENGTH-1, -1, -1), col_constraint_str):
                column_display[row_idx][col_idx] = ch
                col_display_begin = min(col_display_begin, row_idx)
        column_display = column_display[col_display_begin:]
        for row in column_display:
            print("　" * ROW_LENGTH, end='')
            for ch in row:
                if ch == ' ':
                    print("　", end='')
                else:
                    print("０１２３４５６７８９"[int(ch)], end='')
            print()

        # Display Row constraints and puzzle
        # zip([1, 2, 3], [4, 5, 6]) -> [(1, 4), (2, 5), (3, 6)]
        for row_idx, (row_constraint, row) in enumerate(zip(self.row_constraints, self.puzzle)):
            row_constraint_str = ' '.join(map(str, row_constraint))
            print("　" * (ROW_LENGTH - len(row_constraint_str)), end='')
            for ch in row_constraint_str:
                if ch == ' ':
                    print("　", end='')
                else:
                    print("０１２３４５６７８９"[int(ch)], end='')
            for col_idx, cell in enumerate(row):
                if cell == 'o':
                    print('🟦', end='')
                else:
                    if cell == 'x':
                        print('⬜', end='')
                    elif cell == '?':
                        print('❓', end='')
                        self.completed = False
            print()

    def is_complete(self):
        # should not contain "?"
        return not any(any(ch == '?' for ch in row) for row in self.puzzle)

    @staticmethod
    def constraint_match(constaint, line):
        """ Check if a given line matches a constraint

        Args:
            constaint (list of int): constraint
            line (list of str): line to check

        Returns:
            bool: whether the line matches the constraint
        """

        if "?" in line:
            return False

        rle = []
        for c in line:
            if not rle or rle[-1][0] != c:
                rle.append([c, 1])
            else:
                rle[-1][1] += 1
        if constaint == [0]:
            constaint = []
        return constaint == [len(list(v)) for k, v in groupby(line) if k == 'o']

    def is_correct(self):
        """Check if the puzzle is correct.

        A puzzle is correct if it's complete and there's no constraint conflict.

        Returns:
            bool: whether the puzzle is correct
        """

        for constraint, row in zip(self.row_constraints, self.puzzle):
            if not self.constraint_match(constraint, row):
                return False

        for col_idx, col_constraint in enumerate(self.col_constraints):
            col = [row[col_idx] for row in self.puzzle]
            if not self.constraint_match(col_constraint, col):
                return False
        return True


if __name__ == "__main__":
    # Instantiate (實體化)
    gameA = NonoGame("../testcases/5x5/0.in")
    gameA.puzzle = [
        ['x', 'o', 'x', 'x', 'o'],
        ['x', 'o', 'x', 'x', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
        ['x', 'o', 'x', 'x', 'x'],
        ['x', 'x', 'x', 'x', 'o'],
    ]
    gameA.print()
    print(gameA.is_correct())
