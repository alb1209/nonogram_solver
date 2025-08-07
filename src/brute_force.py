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
    def get_nums(line):
        nums, cnt = [], 0
        lsts = 0
        for ch in line:
            if ch == 'o':
                cnt += 1
            elif ch == 'x':
                if cnt:
                    nums.append(cnt)
                    cnt = 0
            else:
                lsts = cnt
                break
        else:
            if cnt:
                nums.append(cnt)

        return nums, lsts

    def is_prefix(nums, cons):
        if len(nums) > len(cons):
            return False

        for i in range(len(nums)):
            if nums[i] != cons[i]:
                return False

        return True

    def can_fit(line, cons):
        nums, lsts = get_nums(line)
        if not is_prefix(nums, cons):
            return False

        id = len(nums)
        if lsts:
            if id >= len(cons) or lsts > cons[id]:
                return False
            rem = [cons[id]-lsts] + cons[id+1:]
        else:
            rem = cons[id:]
        if not rem:
            return True
        need = sum(rem)+len(rem)-1

        return line.count('?') >= need

    cur_row, cur_col = game.puzzle[x], [
        game.puzzle[r][y] for r in range(game.n)]
    correct_row, correct_col = game.row_constraints[x], game.col_constraints[y]

    return can_fit(cur_row, correct_row) and can_fit(cur_col, correct_col)


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
                check = check_possibilities(pos, True) and check_possibilities(pos, False)
                if check:
                    return True
                
    return 0
