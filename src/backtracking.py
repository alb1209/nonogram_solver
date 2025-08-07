from game import NonoGame
from util import *


def backtracking(game: NonoGame):
    search_count = 0

    def dfs(game: NonoGame, pos: int):
        nonlocal search_count
        search_count += 1

        if pos == game.n * game.m:
            return True
        x, y = pos // game.m, pos % game.m

        for ele in range(2):
            if ele:
                game.puzzle[x][y] = "x"
            else:
                game.puzzle[x][y] = "o"

            if checking_element_in_right_pos(game, x, y) and dfs(game, pos + 1):
                return True
            game.puzzle[x][y] = "?"
        return False

    dfs(game, 0)
    print(game.puzzle)
    return search_count


def backtracking_v2(game: NonoGame):
    #　先搜尋已經確定的答案，直到沒有一個答案可以確定後，在隨機猜一個答案
    #print(game.puzzle, game.row_constraints, game.col_constraints)

    def find_possibilities(game, pos):
        x, y = pos // game.m, pos % game.m
        re = []
        for i in ["o", "x"]:
            game.puzzle[x][y] = i
            if checking_element_in_right_pos(x, y):
                re.append(i)
        return re

    def check_possibilities(game, pos, row_col):
        x, y = pos // game.m, pos % game.m
        if row_col:
            for i in range(x * game.m, pos):
                dfs(game, i, True, False)
        else:
            for i in range(x):
                dfs(game, game.m * i + y, False, True)

    def dfs(game: NonoGame, pos: int, row: bool, col: bool):

        x, y = pos // game.m, pos % game.m
        if game.puzzle[x][y] != "?":
            return True

        # Find all possibilities in each uncertain block.
        possibilities = find_possibilities(pos)

        # If there's one block has no possibility, return False.
        if not possibilities:
            return False
        # While there's one block has only one possibility, fill it.
        elif len(possibilities) == 1:
            game.puzzle[x][y] = possibilities[0]
            if row == col == True:
                check_possibilities(pos, True)
                check_possibilities(pos, False)
                return dfs(game, pos + 1, True, True)
            return check_possibilities(pos, not row)
        # If there's no block has only one possibility, guess it and do next round.
        else:
            if row == col == True:
                dfs(game, pos + 1, True, True)
            elif row or col:
                return True

            for i in ["o", "x"]:
                game.puzzle[x][y] = i
                check = check_possibilities(
                    pos, True) and check_possibilities(pos, False)
                if check:
                    return True

    return 0
