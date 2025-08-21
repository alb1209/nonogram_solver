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

    memory_row = [generate_all_possibility_given_constaints(game.row_constraints[i], game.m) for i in range(game.n)]
    memory_col = [generate_all_possibility_given_constaints(game.col_constraints[i], game.n) for i in range(game.m)]
    # print(memory_row, len(memory_row))
    # print(memory_col, len(memory_col))
    def find_possibilities(game:NonoGame, pos: int, row_col: bool):
        if row_col:
            nonlocal memory_row
            all_possibility = memory_row[pos]
            line = game[pos]
        else:
            nonlocal memory_col
            all_possibility = memory_col[pos]
            line = [game[i][pos] for i in range(game.n)]
            # if pos == 2:
            #     print(line, all_possibility)

        possibilities = [set() for _ in range(len(line))]
        for possible_line in all_possibility:
            flag = True
            for a, b in zip(possible_line, line):
                if b != '?' and a != b:
                    flag = False
            if flag:
                for i in range(len(line)):
                    possibilities[i].add(possible_line[i])
        #print(possibilities)
        return possibilities
    

    def memorize(x, y, patern):
        nonlocal memory_col, memory_row
        cur = 0
        history_memory_row, history_memory_col = [], []
        while cur != len(memory_row[x]):
            if memory_row[x][cur][y] != patern:
                history_memory_row.append(memory_row[x].pop(cur))
            else:
                cur += 1
        
        cur = 0
        while cur != len(memory_col[y]):
            if memory_col[y][cur][x] != patern:
                history_memory_col.append(memory_col[y].pop(cur))
            else:
                cur += 1

        return [history_memory_row, x], [history_memory_col, y]

    def _recover(game: NonoGame, history_place: List[int], history_memory_row: List, history_memory_col: List):

        for memory, pos in history_memory_row:
            memory_row[pos].extend(memory)

        for memory, pos in history_memory_col:
            memory_col[pos].extend(memory)
        
        for x, y in history_place:
            game.puzzle[x][y] = "?"

    
    search_count = 0
    def _dfs(game: NonoGame):
        nonlocal search_count, memory_row, memory_col
        #print(memory_row)
        #print(memory_col)
        search_count += 1
        history_place = []
        # Find all possibilities in each uncertain block.
        not_solved = []
        pos_row = []
        pos_col = []
        history_memory_row, history_memory_col  = [], []
        for x in range(game.n):
            pos_row.append(find_possibilities(game, x, True))

        
        for y in range(game.m):
            pos_col.append(find_possibilities(game, y, False))
        
        
        for x in range(game.n):
            for y in range(game.m):
                # print(pos_row, pos_col)
                possibilities = list(pos_row[x][y] & pos_col[y][x])
                if game[x][y] != "?":
                    continue
                if len(possibilities) == 0:
                    # If there's one block has no possibility, return False.
                    _recover(game, history_place, history_memory_row, history_memory_col)
                    return False
                elif len(possibilities) == 1:
                    # While there's one block has only one possibility, fill it.
                    game.puzzle[x][y] = possibilities[0]
                    history_place.append((x, y))
                    a, b = memorize(x, y, possibilities[0])
                    history_memory_row.append(a)
                    history_memory_col.append(b)
                else:
                    not_solved.append((x, y))

        
        #print(history_memory_row, history_memory_col)
        # If there's no block has only one possibility, guess it and do next round.
        if len(not_solved) == 0:
            return search_count
        else:
            #print(not_solved[0])
            x, y = not_solved[0][0], not_solved[0][1]
            history_place.append((x, y))
            
            for guess in "ox":
                game.puzzle[x][y] = guess
                
                a, b = memorize(x, y, guess)
                history_memory_row.append(a)
                history_memory_col.append(b)
                # print(memory_row, ":", history_memory_row)
                # print(memory_col, ":", history_memory_col)
                # print(1)
                result = _dfs(game)
                if result:
                    return search_count
                memory_row[x].extend(history_memory_row[-1][0])
                memory_col[y].extend(history_memory_col[-1][0])
                history_memory_row.pop(-1)
                history_memory_col.pop(-1)
                # print(memory_row, ":", history_memory_row)
                # print(memory_col, ":", history_memory_col)
                # print(2)

            
            #print(history_memory_row, history_memory_col)
            _recover(game, history_place, history_memory_row, history_memory_col)
            return False
    _dfs(game)
    game.print()
    return search_count
    # return backtracking_v2(game)






def backtracking_v4(game: NonoGame):
    # 1. 每一個position就呼叫 generate_all_possibility_given_constaints() 實在是太慢了，
    #    因為你要刪除跟現在盤面所牴觸的可能，每個row跟每個col只要做一次就好，所以請你修改整個城市碼，
    #    使得同個row / col的限制只需要算一次就好。
    #    O(nm(2^n+2^m)) -> O(n2^n + m2^m)
    # 2. generate_all_possibility_given_constaints 實在是太慢了，直接給現在的盤面跟限制，產生出來她的所有可能
    # 3. 這個 (盤面 -> 所有可能) 的轉換可以用 memoization (記憶化) 來儲存
    memory_row = [generate_all_possibility_given_constaints(game.row_constraints[i], game.m) for i in range(game.n)]
    memory_col = [generate_all_possibility_given_constaints(game.col_constraints[i], game.n) for i in range(game.m)]
    print(memory_row)
    print(memory_col)
    # print(memory_row, len(memory_row))
    # print(memory_col, len(memory_col))
    def find_possibilities(game:NonoGame, pos: int, row_col: bool):
        if row_col:
            constraints = game.row_constraints[pos]
            line = game[pos]
            memories = memory_row[pos]
        else:
            constraints = game.col_constraints[pos]
            line = [game[i][pos] for i in range(game.n)]
            memories = memory_col[pos]
        need_change = []
        all_possibilities, history_memory = generate_all_possibility_given_constaints_and_board_v2(constraints, line, memories)
        
        for i in all_possibilities:
            if len(i) == 1:
                need_change.append((pos, *i))
        print(all_possibilities, need_change)
        return need_change
    

    

    def _recover(game: NonoGame, history_place: List[int]):
        for pos in history_place:
            not_solved.add(pos)
            x, y = pos // game.m, pos % game.m
            game.puzzle[x][y] = "?"

    not_solved = set(range(game.m * game.n))
    search_count = 0
    def _dfs(game: NonoGame):
        nonlocal search_count, not_solved
        search_count += 1
        history_place = []
        # Find all possibilities in each uncertain block.
        
        change_unit = {}
        history_memory_row, history_memory_col  = [], []
        
        for i in range(game.n):
            need_change = find_possibilities(game, i, True)
            for cur, patern in need_change:
                pos = i * game.m + cur
                change_unit[pos] = patern
        
        for i in range(game.m):
            need_change = find_possibilities(game, i, False)
            for cur, patern in need_change:
                pos = i * game.m + cur
                if pos in change_unit:
                    if change_unit[pos] != patern:
                        return False
                else:
                    change_unit[pos] = patern
        
        for pos, patern in change_unit.items():
            x, y = pos // game.m, pos % game.n
            game.puzzle[x][y] = patern
            print(pos, x, y, patern)
            not_solved.remove(pos)
            history_place.append(pos)
        game.print()
        if not_solved:
            pos = not_solved.pop()
            history_place.append(pos)
            x, y = pos // game.m, pos % game.m
            for i in "ox":
                game.puzzle[x][y] = i
                print(i)
                if _dfs(game):
                    return search_count
            _recover(game, history_place)
            return False
        return search_count
            



    _dfs(game)
    game.print()
    return search_count
    # return backtracking_v2(game)


    