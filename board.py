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
        self._edges_remaining = 2 * x_dimension * y_dimension + x_dimension + y_dimension
        self._x_bound = x_dimension * 2
        self._y_bound = y_dimension * 2
        self.board = [[False for i in range(self._y_bound + 1)] for i in range(self._x_bound + 1)]

    def move(self, x_coor, y_coor, user):
        if self._edge_is_out_of_bounds(x_coor, y_coor):
            print(f"({x_coor}, {y_coor}) is out of the x-bound {self._x_bound} and/or y-bound {self._y_bound}.")
            raise OutOfBounds()
        x_coor_is_even = x_coor % 2 == 0
        y_coor_is_even = y_coor % 2 == 0
        # parity of coordinates must be different for valid edge
        if x_coor_is_even == y_coor_is_even:
            print(f"({x_coor}, {y_coor}) is an invalid coordinate. x and y must have opposite parity.")
            raise InvalidCoordinate()
        if self.board[x_coor][y_coor]:
            print(f"({x_coor}, {y_coor}) is an invalid coordinate. The edge is already taken.")
            raise EdgeAlreadyTaken()

        self._fill_edge(x_coor, y_coor)
        # horizontal edge filled
        if x_coor_is_even and not y_coor_is_even:
            # check top box
            top_box_x_coor, top_box_y_coor = x_coor - 2, y_coor - 1
            if (not self._box_is_out_of_bounds(top_box_x_coor, top_box_y_coor) 
                and self._is_box_full(top_box_x_coor , top_box_y_coor)):
                self._assign_box(top_box_x_coor , top_box_y_coor, user)
            # check bottom box
            bottom_box_x_coor, bottom_box_y_coor = x_coor, y_coor - 1
            if (not self._box_is_out_of_bounds(bottom_box_x_coor, bottom_box_y_coor)
                and self._is_box_full(bottom_box_x_coor , bottom_box_y_coor)):
                self._assign_box(bottom_box_x_coor , bottom_box_y_coor, user)
        # vertical edge filled
        else:
            # check left box
            left_box_x_coor, left_box_y_coor = x_coor - 1, y_coor - 2
            if (not self._box_is_out_of_bounds(left_box_x_coor, left_box_y_coor)
                and self._is_box_full(left_box_x_coor , left_box_y_coor)):
                self._assign_box(left_box_x_coor , left_box_y_coor, user)
            # check right box
            right_box_x_coor, right_box_y_coor = x_coor - 1, y_coor
            if (not self._box_is_out_of_bounds(right_box_x_coor, right_box_y_coor)
                and self._is_box_full(right_box_x_coor , right_box_y_coor)):
                self._assign_box(right_box_x_coor , right_box_y_coor, user)

    def game_over(self):
        return self._edges_remaining <= 0
    
    """
    Assumes the coordinate is a valid edge
    """
    def _fill_edge(self, x_coor, y_coor):
        self.board[x_coor][y_coor] = True
        self._edges_remaining -= 1

    """
    Assigns box to a player. Assumes (x_coor, y_coor) is top left coordinate of box and the box edges are filled.
    """
    def _assign_box(self, x_coor, y_coor, user):
        self.board[x_coor][y_coor] = user

    """
    Checks if a box is full. The box being checked has the top left dot at (x_coor, y_coor).
    """
    def _is_box_full(self, x_coor, y_coor):
        return (self.board[x_coor][y_coor + 1] and self.board[x_coor + 2][y_coor + 1]
            and self.board[x_coor + 1][y_coor] and self.board[x_coor + 1][y_coor + 2])
        
    def _edge_is_out_of_bounds(self, x_coor, y_coor):
        return x_coor < 0 or x_coor > self._x_bound or y_coor < 0 or y_coor > self._y_bound

    def _box_is_out_of_bounds(self, x_coor, y_coor):
        return x_coor < 0 or x_coor > (self._x_bound - 2) or y_coor < 0 or y_coor > (self._y_bound - 2)



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
        def one_box_filled_with_vertical_edge():
            board = Board(2, 3)
            board.move(0, 1, True)
            board.move(2, 1, True)
            board.move(1, 2, True)
            self.assertFalse(board.board[0][0])
            self.assertFalse(board.board[0][2])
            board.move(1, 0, True)
            self.assertTrue(board.board[0][0])
            self.assertFalse(board.board[0][2])
        def two_boxes_filled_with_vertical_edge():
            board = Board(2, 3)
            board.move(0, 3, True)
            board.move(0, 5, True)
            board.move(2, 3, True)
            board.move(2, 5, True)
            board.move(1, 2, True)
            board.move(1, 6, True)
            self.assertFalse(board.board[0][2])
            self.assertFalse(board.board[0][4])
            board.move(1, 4, True)
            self.assertTrue(board.board[0][2])
            self.assertTrue(board.board[0][4])
        def one_box_filled_with_horizontal_edge():
            board = Board(2, 3)
            board.move(3, 0, True)
            board.move(3, 2, True)
            board.move(2, 1, True)
            self.assertFalse(board.board[2][0])
            board.move(4, 1, True)
            self.assertTrue(board.board[2][0])
        def two_boxes_filled_with_horizontal_edge():
            board = Board()
            board.move(1, 0, True)
            board.move(3, 0, True)
            board.move(1, 2, True)
            board.move(3, 2, True)
            board.move(0, 1, True)
            board.move(4, 1, True)
            self.assertFalse(board.board[0][0])
            self.assertFalse(board.board[2][0])
            board.move(2, 1, True)
            self.assertTrue(board.board[0][0])
            self.assertTrue(board.board[2][0])
        one_box_filled_with_vertical_edge()
        two_boxes_filled_with_vertical_edge()
        one_box_filled_with_horizontal_edge()
        two_boxes_filled_with_horizontal_edge()
    
    def test_game_over(self):
        board = Board(1, 1)
        self.assertFalse(board.game_over())
        board.move(1, 0, True)
        board.move(1, 2, True)
        board.move(0, 1, True)
        self.assertFalse(board.game_over())
        board.move(2, 1, True)
        self.assertTrue(board.game_over())

if __name__ == "__main__":
    unittest.main()

            

        
