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
    def __init__(self, x_dimension=4, y_dimension=5):
        self._rows = y_dimension
        self._cols = x_dimension
        self._edges_remaining = 2 * x_dimension * y_dimension + x_dimension + y_dimension
        self._row_bound = y_dimension * 2
        self._col_bound = x_dimension * 2
        self.board = [[False for i in range(self._col_bound + 1)] for i in range(self._row_bound + 1)]

    def move(self, row, col, is_player_one):
        if self.edge_is_out_of_bounds(row, col):
            print(f"({row}, {col}) is out of the x-bound {self._row_bound} and/or y-bound {self._col_bound}.")
            raise OutOfBounds()
        row_is_even = row % 2 == 0
        col_is_even = col % 2 == 0
        # parity of coordinates must be different for valid edge
        if row_is_even == col_is_even:
            print(f"({row}, {col}) is an invalid coordinate. x and y must have opposite parity.")
            raise InvalidCoordinate()
        if self.board[row][col]:
            print(f"({row}, {col}) is an invalid coordinate. The edge is already taken.")
            raise EdgeAlreadyTaken()

        self._fill_edge(row, col)
        # whether the move filled a box
        box_taken = False
        # horizontal edge filled
        if row_is_even and not col_is_even:
            # check top box
            top_box_row, top_box_col = row - 2, col - 1
            if (not self._box_is_out_of_bounds(top_box_row, top_box_col) 
                and self._is_box_full(top_box_row , top_box_col)):
                box_taken = True
                self._assign_box(top_box_row , top_box_col, is_player_one)
            # check bottom box
            bottom_box_row, bottom_box_col = row, col - 1
            if (not self._box_is_out_of_bounds(bottom_box_row, bottom_box_col)
                and self._is_box_full(bottom_box_row , bottom_box_col)):
                box_taken = True
                self._assign_box(bottom_box_row , bottom_box_col, is_player_one)
        # vertical edge filled
        else:
            # check left box
            left_box_row, left_box_col = row - 1, col - 2
            if (not self._box_is_out_of_bounds(left_box_row, left_box_col)
                and self._is_box_full(left_box_row , left_box_col)):
                box_taken = True
                self._assign_box(left_box_row , left_box_col, is_player_one)
            # check right box
            right_box_row, right_box_col = row - 1, col
            if (not self._box_is_out_of_bounds(right_box_row, right_box_col)
                and self._is_box_full(right_box_row , right_box_col)):
                box_taken = True
                self._assign_box(right_box_row , right_box_col, is_player_one)
        return box_taken

    def is_edge(self, row, col):
        row_is_even = row % 2 == 0
        col_is_even = col % 2 == 0
        return not row_is_even == col_is_even

    def edge_taken(self, row, col):
        return self.board[row][col]

    def game_over(self):
        return self._edges_remaining <= 0

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._cols

    @property
    def row_bound(self):
        return self._row_bound

    @property
    def column_bound(self):
        return self._col_bound
    
    """
    Assumes the coordinate is a valid edge
    """
    def _fill_edge(self, row, col):
        self.board[row][col] = True
        self._edges_remaining -= 1

    """
    Assigns box to a player. Assumes (x_coor, y_coor) is top left coordinate of box and the box edges are filled.
    """
    def _assign_box(self, row, col, is_player_one):
        if is_player_one:
            self.board[row][col] = True
        else:
            self.board[row + 1][col + 1] = True

    """
    Checks if a box is full. The box being checked has the top left dot at (x_coor, y_coor).
    """
    def _is_box_full(self, row, col):
        return (self.board[row][col + 1] and self.board[row + 2][col + 1]
            and self.board[row + 1][col] and self.board[row + 1][col + 2])
        
    def edge_is_out_of_bounds(self, row, col):
        return row < 0 or row > self._row_bound or col < 0 or col > self._col_bound

    def _box_is_out_of_bounds(self, row, col):
        return row < 0 or row > (self._row_bound - 2) or col < 0 or col > (self._col_bound - 2)

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
            board = Board(3, 2)
            board.move(0, 1, True)
            board.move(2, 1, True)
            board.move(1, 2, True)
            self.assertFalse(board.board[0][0])
            self.assertFalse(board.board[0][2])
            board.move(1, 0, True)
            self.assertTrue(board.board[0][0])
            self.assertFalse(board.board[0][2])
        def two_boxes_filled_with_vertical_edge():
            board = Board(3, 2)
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
            board = Board(3, 2)
            board.move(3, 0, False)
            board.move(3, 2, False)
            board.move(2, 1, False)
            self.assertFalse(board.board[2][0])
            self.assertFalse(board.board[3][1])
            board.move(4, 1, False)
            self.assertFalse(board.board[2][0])
            self.assertTrue(board.board[3][1])
        def two_boxes_filled_with_horizontal_edge():
            board = Board()
            board.move(1, 0, False)
            board.move(3, 0, False)
            board.move(1, 2, False)
            board.move(3, 2, False)
            board.move(0, 1, False)
            board.move(4, 1, False)
            self.assertFalse(board.board[0][0])
            self.assertFalse(board.board[1][1])
            self.assertFalse(board.board[2][0])
            self.assertFalse(board.board[3][1])
            board.move(2, 1, False)
            self.assertFalse(board.board[0][0])
            self.assertFalse(board.board[2][0])
            self.assertTrue(board.board[1][1])
            self.assertTrue(board.board[3][1])
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

            

        
