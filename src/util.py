from game import NonoGame


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
