from game import NonoGame
import time
def test_5x5(solver: callable):
    test_cases = [f"../testcases/5x5/{i}.in" for i in range(5)]
    for test_case in test_cases:
        game = NonoGame(test_case)
        start = time.monotonic()
        search_count = solver(game)
        end = time.monotonic()
        print(f"{test_case:30s} Cost: {end-start : 8.2f}s State Cnt: {search_count:10d} Judge: {game.is_correct()}")


def main():
    from brute_force import pure_brute_force
    test_5x5(pure_brute_force)

if __name__ == "__main__": 
    main()