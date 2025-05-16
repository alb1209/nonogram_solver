from game import NonoGame
from itertools import product
import time
from itertools import batched


def pure_brute_force(game: NonoGame):
    search_count = 0
    for idx, trial in enumerate(product(*["ox" for _ in range(25)])):
        guess = list(batched(trial, 5))
        game.puzzle = guess
        search_count += 1
        if game.is_correct():
            break
    return search_count


def true_brute_force(game: NonoGame):
    """
    枚舉每一個 row constraints 的可能性
    在用 product 暴力搜尋
    你應該要用到兩次 product
    """
    circles = ["o", "oo", "ooo", "oooo", "ooooo"]
    needed_rows = []

    for row in game.row_constraints:
        needed = []
        for i in row:
            needed.append(circles[i - 1])
        for i in range(game.m - sum(row)):
            needed.append("x")
        needed_rows.append(list(product(*needed)))

    search_count = 0

    for idx, trial in enumerate(product(*needed_rows)):
        guess = list(trial)
        game.puzzle = guess
        search_count += 1
        if game.is_correct():
            break
    return search_count
