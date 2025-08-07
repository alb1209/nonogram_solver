# test_calculator.py

import unittest
import util

class TestPossibilitiesGenerator(unittest.TestCase):
    def test_gen_v1(self):
        constraint = [2, 1]
        result = util.generate_all_possibility_given_constaints(constraint, 5)
        sorted(result)
        self.assertEqual(result, [['o', 'o', 'x', 'o', 'x'], ['o', 'o', 'x', 'x', 'o'], ['x', 'o', 'o', 'x', 'o']])

    def test_gen_v2(self):
        board = ['?', '?', '?', '?', '?']
        constraint = [2, 1]
        result = util.generate_all_possibility_given_constaints_and_board(constraint, board)
        sorted(result)
        self.assertEqual(result, [['o', 'o', 'x', 'o', 'x'], ['o', 'o', 'x', 'x', 'o'], ['x', 'o', 'o', 'x', 'o']])


        board = ['?', 'o', '?', '?', '?']
        constraint = [1, 2]
        result = util.generate_all_possibility_given_constaints_and_board(constraint, board)
        self.assertEqual(result, [['x', 'o', 'x', 'o', 'o']])


if __name__ == '__main__':
    unittest.main()
