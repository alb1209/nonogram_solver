class NonoGame:

    # dunder: double under
    def __init__(self, filepath):
        # r - read (default)
        # w - write
        self.row_constraints = []
        self.col_constraints = []
        # ~= fin = open(filepath)
        with open(filepath) as fin:
            n, m = map(int, fin.readline().strip().split())
            self.n, self.m = n, m
            print(n, m)
            # Row contraints
            for _ in range(n):
                tmp = list(map(int, fin.readline().strip().split()))
                self.row_constraints.append(tmp)
            # Column contraints
            for _ in range(m):
                tmp = list(map(int, fin.readline().strip().split()))
                self.col_constraints.append(tmp)
        
        self.puzzle = [['?' for _ in range(m)] for _ in range(n)]
        # self.n, self.m = 5, 5
    
    def print(self):
        COL_LENGTH = 15
        ROW_LENGTH = 15

        # Display Column constraints
        col_display_begin = COL_LENGTH
        column_display = [[' ' for _ in  range(self.m)] for _ in range(COL_LENGTH)]
        for col_idx, col_constraint in enumerate(self.col_constraints):
            col_constraint_str = ' '.join(map(str, col_constraint))
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
        for row_constraint, row in zip(self.row_constraints, self.puzzle):
            row_constraint_str = ' '.join(map(str, row_constraint))
            print("　" * (ROW_LENGTH - len(row_constraint_str)), end='')
            for ch in row_constraint_str:
                if ch == ' ':
                    print("　", end='')
                else:
                    print("０１２３４５６７８９"[int(ch)], end='')
            for cell in row:
                if cell == '?':
                    print('❓', end='')
                elif cell == 'x':
                    print('⬜', end='')
                elif cell == 'o':
                    print('🟦', end='')
            print()
    
    def is_complete(self):
        # should not contain "?"
        # TODO
        pass

    def is_correct(self):
        # complete and there's no constraint conflict
        # TODO
        pass


if __name__ == "__main__":
    # Instantiate (實體化)
    gameA = NonoGame("../testcases/5x5/0.in")
    gameA.puzzle = [
        ['o', 'o', 'o', 'x', 'x'],
        ['x', '?', '?', '?', 'x'],
        ['x', 'x', 'o', 'o', 'o'],
        ['o', 'x', 'x', '?', 'o'],
        ['x', 'x', 'x', 'x', 'o'],
    ]
    gameA.print()

