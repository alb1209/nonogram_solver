from game import NonoGame
from util import *
from typing import List

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

    def find_possibilities(game:NonoGame, pos: int):
        x, y = pos // game.m, pos % game.m
        if game[x][y] != '?':
            return game[x][y]
        else:
            row_possible = set()
            for possible_row in generate_all_possibility_given_row(game.row_constraints[x], game.m):
                flag = True
                for a, b in zip(possible_row, game[x]):
                    if b != '?' and a != b:
                        flag = False
                if flag:
                    row_possible.add(possible_row[y])
            
            col_possible = set()
            game_col_y = [game[i][y] for i in range(game.n)]
            for possible_col in generate_all_possibility_given_row(game.col_constraints[y], game.n):
                flag = True
                for a, b in zip(possible_col, game_col_y):
                    if b != '?' and a != b:
                        flag = False
                if flag:
                    col_possible.add(possible_col[x])
            return list(row_possible & col_possible)

    # def check_possibilities(game, pos, row_col):
    #     x, y = pos // game.m, pos % game.m
    #     if row_col:
    #         for i in range(x * game.m, pos):
    #             dfs(game, i, True, False)
    #     else:
    #         for i in range(x):
    #             dfs(game, game.m * i + y, False, True)

    # def dfs(game: NonoGame, pos: int, row: bool, col: bool):

    #     x, y = pos // game.m, pos % game.m
    #     if game.puzzle[x][y] != "?":
    #         return True

    #     # Find all possibilities in each uncertain block.
    #     possibilities = find_possibilities(pos)

    #     # If there's one block has no possibility, return False.
    #     if not possibilities:
    #         return False
    #     # While there's one block has only one possibility, fill it.
    #     elif len(possibilities) == 1:
    #         game.puzzle[x][y] = possibilities[0]
    #         if row == col == True:
    #             check_possibilities(pos, True)
    #             check_possibilities(pos, False)
    #             return dfs(game, pos + 1, True, True)
    #         return check_possibilities(pos, not row)
    #     # If there's no block has only one possibility, guess it and do next round.
    #     else:
    #         if row == col == True:
    #             dfs(game, pos + 1, True, True)
    #         elif row or col:
    #             return True

    #         for i in ["o", "x"]:
    #             game.puzzle[x][y] = i
    #             check = check_possibilities(
    #                 pos, True) and check_possibilities(pos, False)
    #             if check:
    #                 return True

    def _recover(game: NonoGame, history_place: List[int]):
        for x, y in history_place:
            game.puzzle[x][y] = "?"

    search_count = 0
    def _dfs(game: NonoGame):
        nonlocal search_count
        search_count += 1
        history_place = []
        # Find all possibilities in each uncertain block.
        not_solved = []
        for x in range(game.n):
            for y in range(game.m):
                if game[x][y] == "?":
                    i = game.m * x + y
                    result = find_possibilities(game, i)
                    if len(result) == 0:
                        # If there's one block has no possibility, return False.
                        _recover(game, history_place)
                        return False
                    elif len(result) == 1:
                        # While there's one block has only one possibility, fill it.
                        game.puzzle[x][y] = result[0]
                        history_place.append((x, y))
                    else:
                        not_solved.append(i)
        # If there's no block has only one possibility, guess it and do next round.
        if len(not_solved) == 0:
            return search_count
        else:
            i = not_solved[0]
            x, y = i // game.m, i % game.m
            history_place.append((x, y))
            for guess in "ox":
                game.puzzle[x][y] = guess
                result = _dfs(game)
                if result:
                    return search_count
            _recover(game, history_place)
            return False
    _dfs(game)
    game.print()
    return search_count


