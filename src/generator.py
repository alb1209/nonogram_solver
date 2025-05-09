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

def generate_all_5x5(n_testcases):
    for i in range(n_testcases):
        random_generator(f"../testcases/5x5/{i}.in", 5, 5, prob=(i+1)/(n_testcases+1))

def main():
    random.seed("Live a life you will remember")
    generate_all_5x5(5)

if __name__ == "__main__":
    main()