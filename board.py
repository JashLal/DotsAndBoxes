from collections import defaultdict
import unittest

"""
Custom exception for out of bounds user move
Best practice is to move this to its own file called exceptions.py or errors.py
"""
class OutOfBounds(Exception):
    pass

class InvalidCoordinate(Exception):
    pass

class EdgeAlreadyTaken(Exception):
    pass

class Board:
    def __init__(self, x_dimension=5, y_dimension=4):
        self._x_dimension = x_dimension
        self._y_dimension = y_dimension
        self._x_bound = x_dimension * 2
        self._y_bound = y_dimension * 2
        self.board = [[False for i in range(self._y_bound + 1)] for i in range(self._x_bound + 1)]

    def move(self, x_coor, y_coor, user):
        # out of bounds
        if x_coor < 0 or x_coor > self._x_bound or y_coor < 0 or y_coor > self._y_bound:
            print(f"({x_coor}, {y_coor}) is out of the x-bound {self._x_bound} and/or y-bound {self._y_bound}.")
            raise OutOfBounds()
        x_coor_is_even = x_coor % 2 == 0
        y_coor_is_even = y_coor % 2 == 0
        # parity of coordinates must be different for valid edge
        if x_coor_is_even == y_coor_is_even:
            print(f"({x_coor}, {y_coor}) is an invalid coordinate. x and y must have opposite parity.")
            raise InvalidCoordinate()
        # edge already taken
        if self.board[x_coor][y_coor]:
            print(f"({x_coor}, {y_coor}) is an invalid coordinate. The edge is already taken.")
            raise EdgeAlreadyTaken()
        # fill in the edge
        self.board[x_coor][y_coor] = True
        # fill in the square if valid

class TestBoard(unittest.TestCase):
    def test_move_invalid(self):
        board = Board()
        def out_of_bounds():
            self.assertRaises(OutOfBounds, board.move, -1, 0, True)
            self.assertRaises(OutOfBounds, board.move, 11, 0, True)
            self.assertRaises(OutOfBounds, board.move, 0, -1, True)
            self.assertRaises(OutOfBounds, board.move, 0, 9, True)
        def equal_parity():
            self.assertRaises(InvalidCoordinate, board.move, 0, 4, True)
            self.assertRaises(InvalidCoordinate, board.move, 1, 3, True)
        def edge_already_taken():
            board.move(0, 1, True)
            self.assertRaises(EdgeAlreadyTaken, board.move, 0, 1, True)
            board.move(9, 8, True)
            self.assertRaises(EdgeAlreadyTaken, board.move, 9, 8, True)
        out_of_bounds()
        equal_parity()
        edge_already_taken()

    def test_move_valid(self):
        pass

if __name__ == "__main__":
    unittest.main()

            

        
