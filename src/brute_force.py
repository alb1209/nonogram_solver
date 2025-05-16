from game import NonoGame
from itertools import product
import time
from itertools import batched, permutations


def brute_force_v1(game: NonoGame):
    search_count = 0
    for idx, trial in enumerate(product(*["ox" for _ in range(25)])):
        guess = list(batched(trial, 5))
        game.puzzle = guess
        search_count += 1
        if game.is_correct():
            break
    return search_count


def brute_force_v2(game: NonoGame):
    """
    枚舉每一個 row constraints 的可能性
    在用 product 暴力搜尋
    你應該要用到兩次 product
    """
    circles = ["o", "oo", "ooo", "oooo", "ooooo"]
    needed_rows = []

    for row in game.row_constraints:
        needed = []
        if row == [0]:
            needed_rows.append([['x'] * game.m])
        else:
            for i in row:
                needed.append(circles[i - 1])
            for i in range(game.m - sum(row)):
                needed.append("x")
            tmp = set()
            for perm in permutations(needed):
                tmp.add(tuple("".join(perm)))
            needed_rows.append(tmp)
    search_count = 0

    for idx, trial in enumerate(product(*needed_rows)):
        guess = list(trial)
        game.puzzle = guess
        search_count += 1
        if game.is_correct():
            break
    game.print()
    return search_count


def generate_all_possibility_given_row(row_constraint, m):
    total_result = []
    def rec(row_top, current, current_len):
        if current_len > m:
            return
        if row_top == len(row_constraint):
            if m - current_len > 0:
                result = current + ['x' * (m - current_len)]
            else:
                result = current
            total_result.append(list("".join(result)))
            return

        for i in range(0 if current_len == 0 else 1, m):
            current.append('x' * i)
            current.append('o' * row_constraint[row_top])
            rec(row_top + 1, current, current_len + i + row_constraint[row_top])
            current.pop()
            current.pop()
    rec(0, [], 0)
    return total_result


def brute_force_v3(game: NonoGame):
    needed_rows = []
    for row in game.row_constraints:
        needed_rows.append(generate_all_possibility_given_row(row, game.m))
        print(len(needed_rows[-1]), end=', ')
    print()
    search_count = 0

    for idx, trial in enumerate(product(*needed_rows)):
        guess = list(trial)
        game.puzzle = guess
        search_count += 1
        if game.is_correct():
            break
    game.print()
    return search_count

def backtracking(game: NonoGame):
    search_count = 0
    def dfs(game: NonoGame, pos: int):
        nonlocal search_count
        search_count += 1

        if pos == game.n * game.m:
            return True
        x, y = pos // game.m, pos % game.m

    dfs(game, 0)
    return 