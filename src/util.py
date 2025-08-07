from game import NonoGame
from typing import List

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

def generate_all_possibility_given_constaints(constraint: List[int], block_size: int):
    """
    根據 Nonogram 的 block 長度限制 (constraint) 與整行格數 (block_size)，
    生成該行所有可能的排列組合。
    
    參數：
    - constraint: List[int]，表示每個連續填滿區段的長度。例如 [3,1] 意味著先有 3 格實心，再至少空 1 格，然後再 1 格實心。
    - block_size: int，該行總共的格數。

    回傳值：
    - total_result: List[List[str]]，每一個子 List[str] 代表一種可能的排列，以 'x' 表示空格，以 'o' 表示實心格。
    """
    total_result = []  # 最終所有可能排列的結果清單

    def rec(row_top: int, current: List[str], current_len: int):
        """
        遞迴函式，依序放入每個 constraint 區段，並在區段間插入至少一格空白（除非是第一段）。

        參數：
        - row_top: int，目前處理到 constraint 的索引
        - current: List[str]，目前已經拼好的字串片段清單（尚未 join）
        - current_len: int，目前拼好的片段總長度
        """
        # 如果當前長度已經超過整行格數，提前結束遞迴
        if current_len > block_size:
            return

        # 當所有 constraint 區段都放完後
        if row_top == len(constraint):
            # 若剩餘格數大於 0，就補足剩下的空白格並加入結果
            if block_size - current_len > 0:
                result = current + ['x' * (block_size - current_len)]
            else:
                result = current
            # 把拼完的字串片段 join 後，拆成單格字元列表存入 total_result
            total_result.append(list("".join(result)))
            return

        # 對於第 row_top 個區段，決定「空白」的格數
        # 第一個區段前可以是 0 格空白，其後每個區段前至少要 1 格空白
        for i in range(0 if current_len == 0 else 1, block_size):
            # 加入 i 格空白
            current.append('x' * i)
            # 加入 constraint[row_top] 格實心
            current.append('o' * constraint[row_top])
            # 遞迴到下一個區段，更新已用長度
            rec(
                row_top + 1,
                current,
                current_len + i + constraint[row_top]
            )
            # 回溯：彈出剛才加的實心與空白
            current.pop()
            current.pop()

    # 從第 0 個區段開始遞迴，初始沒有片段，長度為 0
    rec(0, [], 0)
    return total_result


def generate_all_possibility_given_constaints_and_board(constraint: List[int], current_boad: List[str]):
    # 根據現在的盤面，算出可能的所有排列
    pass
