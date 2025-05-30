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
            rec(row_top + 1, current, current_len +
                i + row_constraint[row_top])
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


def checking_element_in_right_pos(game: NonoGame, x, y):
    cur_row, cur_col= game.puzzle[x], game.puzzle[y]
    correct_row, correct_col = game.row_constraints[x]+[0], game.col_constraints[y]+[0]

    check = 0
    i = 0
    for ele in cur_row:
        if i > len(correct_row):
            return False
        if check > correct_row[i]: #i==len(...) => RE
            return False

        if ele == "?":
            break

        if ele == "o":
            check += 1
        elif check != 0 and check < correct_row[i]:
            return False
        elif correct_row[i]==0:
            continue
        else:
            i += 1
            check = 0

    if "?" not in cur_row and i!=len(correct_row)-1:
        return False

    check = 0
    i = 0
    for ele in cur_col:
        if i > len(correct_col):
            return False
        if check > correct_col[i]:
            return False
       
        if ele == "?":
            break

        if ele == "o":
            check += 1
        elif check != 0 and check < correct_col[i]:
            return False
        elif correct_col[i]==0:
            continue
        else:
            i += 1
            check = 0

    if "?" not in cur_col and i!=len(correct_col)-1:
        return False
    
    return True


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
