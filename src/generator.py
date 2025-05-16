import random
from itertools import groupby
from game import NonoGame
def random_generator(filepath, n, m, prob=0.2):
    puzzle = [['?' for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            puzzle[i][j] = random.choices(['o', 'x'], [prob, 1-prob])[0]

    row_constriants = []
    for row in puzzle:
        row_constriants.append([len(list(v)) for k, v in groupby(row) if k == 'o'])
    col_constriants = []
    for col in zip(*puzzle):
        col_constriants.append([len(list(v)) for k, v in groupby(col) if k == 'o'])
    
    with open(filepath, "w") as fin:
        print(n, m, file=fin)
        for row in row_constriants:
            if len(row) == 0:
                row = [0]
            print(' '.join(map(str, row)), file=fin)
        for col in col_constriants:
            if len(col) == 0:
                col = [0]
            print(' '.join(map(str, col)), file=fin)

import os
def random_generate(n_testcases, n, m):
    for i in range(n_testcases):
        os.makedirs(f"../testcases/{n}x{m}", exist_ok=True)
        random_generator(f"../testcases/{n}x{m}/{i}.in", n, m, prob=(i+1)/(n_testcases+1))

def main():
    random.seed("Live a life you will remember")
    random_generate(5, 5, 5)
    random_generate(5, 7, 7)
    random_generate(5, 8, 8)
    random_generate(5, 10, 10)
    random_generate(5, 15, 15)
    random_generate(5, 20, 20)

if __name__ == "__main__":
    main()