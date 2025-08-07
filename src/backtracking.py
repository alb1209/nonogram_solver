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
            for possible_row in generate_all_possibility_given_constaints(game.row_constraints[x], game.m):
                flag = True
                for a, b in zip(possible_row, game[x]):
                    if b != '?' and a != b:
                        flag = False
                if flag:
                    row_possible.add(possible_row[y])
            
            col_possible = set()
            game_col_y = [game[i][y] for i in range(game.n)]
            for possible_col in generate_all_possibility_given_constaints(game.col_constraints[y], game.n):
                flag = True
                for a, b in zip(possible_col, game_col_y):
                    if b != '?' and a != b:
                        flag = False
                if flag:
                    col_possible.add(possible_col[x])
            return list(row_possible & col_possible)

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

def backtracking_v3(game: NonoGame):
    # 1. 每一個position就呼叫 generate_all_possibility_given_constaints() 實在是太慢了，
    #    因為你要刪除跟現在盤面所牴觸的可能，每個row跟每個col只要做一次就好，所以請你修改整個城市碼，
    #    使得同個row / col的限制只需要算一次就好。
    #    O(nm(2^n+2^m)) -> O(n2^n + m2^m)
    # 2. generate_all_possibility_given_constaints 實在是太慢了，直接給現在的盤面跟限制，產生出來她的所有可能
    # 3. 這個 (盤面 -> 所有可能) 的轉換可以用 memoization (記憶化) 來儲存
    pass
    # return backtracking_v2(game)