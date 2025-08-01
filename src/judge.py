from game import NonoGame
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
    from brute_force import backtracking, brute_force_v3, brute_force_v2, brute_force_v1
    test(backtracking, 15, 15)

if __name__ == "__main__": 
    main()