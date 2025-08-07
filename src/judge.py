from game import NonoGame
from brute_force import *
from backtracking import *
import time
def test(solver: callable, n, m):
    test_cases = [f"./testcases/{n}x{m}/{i}.in" for i in range(5)]
    for test_case in test_cases:
        game = NonoGame(test_case)
        start = time.monotonic()
        search_count = solver(game)
        end = time.monotonic()
        print(f"{test_case:30s} Cost: {end-start : 8.2f}s State Cnt: {search_count:10d} Judge: {game.is_correct()}")

def main():
    test(backtracking_v2, 20, 20)

if __name__ == "__main__": 
    main()