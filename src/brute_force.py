from game import NonoGame
from itertools import product
from itertools import permutations
from util import *


def brute_force_v1(game: NonoGame):
    search_count = 0
    from itertools import batched
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
