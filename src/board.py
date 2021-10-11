# -*- coding: utf-8 -*-
"""
The game state is represented as a 2x2 matrix of booleans. See the example below.

Graphical Representation:
    0   1
  o---o---o
0 | C | C |
  o---o---o
1  
  o---o---o
2     | U |
  o   o---o

Matrix Representation
  0 1 2 3 4
0 F T F T F
1 T T T T T
2 F T F T F
3 F F F F F
4 F T T T F
5 F F T F T
6 F F F T F

For each box (row, col) in the graph representation, the matrix representation denotes...
(2 * row, 2 * col) --> Player one won the box
(2 * row + 1, 2 * col + 1) --> Player two won the box
(2 * row, 2 * col + 1) --> Top edge taken
(2 * row, 2 * col + 2) --> Bottom edge taken
(2 * row + 1, 2 * col) --> Left edge taken
(2 * row + 2, 2 * col) --> Right edge taken
"""

class Board:
    """Stores the state and handles its manipulation."""
    def __init__(self, cols=4, rows=5):
        self._rows = rows
        self._cols = cols
        self._edges_remaining = 2 * cols * rows + cols + rows
        self.board = [[False] * (2 * cols + 1) for _ in range(2 * rows + 1)]
        self._player_one_score = 0
        self._player_two_score = 0

    def move(self, row, col, player_one_turn):
        """PRE: (row, col) is a valid edge on the board.
        Updates state to reflect the new edge and boxes it may have filled.
        If player_one_turn, player one made the move; otherwise, player two
        Returns: Whether a box was aquired due to the move
        """
        self._fill_edge(row, col)
        # whether the move filled a box
        box_taken = False
        if self.is_horizontal_edge(row, col):
            # check top box
            top_box_row, top_box_col = row - 2, col - 1
            if (not self._box_is_out_of_bounds(top_box_row, top_box_col) 
                and self._is_box_full(top_box_row , top_box_col)):
                box_taken = True
                self._assign_box(top_box_row , top_box_col, player_one_turn)
            # check bottom box
            bottom_box_row, bottom_box_col = row, col - 1
            if (not self._box_is_out_of_bounds(bottom_box_row, bottom_box_col)
                and self._is_box_full(bottom_box_row , bottom_box_col)):
                box_taken = True
                self._assign_box(bottom_box_row , bottom_box_col, player_one_turn)
        else:
            # check left box
            left_box_row, left_box_col = row - 1, col - 2
            if (not self._box_is_out_of_bounds(left_box_row, left_box_col)
                and self._is_box_full(left_box_row , left_box_col)):
                box_taken = True
                self._assign_box(left_box_row , left_box_col, player_one_turn)
            # check right box
            right_box_row, right_box_col = row - 1, col
            if (not self._box_is_out_of_bounds(right_box_row, right_box_col)
                and self._is_box_full(right_box_row , right_box_col)):
                box_taken = True
                self._assign_box(right_box_row , right_box_col, player_one_turn)
        return box_taken
    
    def revert_move(self, row, col):
        """
        Pre: (row, col) is a valid edge
        Updates state to remove the edge and unassign boxes it belongs to.
        Used by the computer's algorithm to determine optimal move.
        """
        self._unfill_edge(row, col)
        if self.is_horizontal_edge(row, col):
            # check top box
            top_box_row, top_box_col = row - 2, col - 1
            if not self._box_is_out_of_bounds(top_box_row, top_box_col):
                self._unassign_box(top_box_row, top_box_col)
            # check bottom box
            bottom_box_row, bottom_box_col = row, col - 1
            if not self._box_is_out_of_bounds(bottom_box_row, bottom_box_col):
                self._unassign_box(bottom_box_row, bottom_box_col)
        else:
            # check left box
            left_box_row, left_box_col = row - 1, col - 2
            if not self._box_is_out_of_bounds(left_box_row, left_box_col):
                self._unassign_box(left_box_row, left_box_col)
            # check right box
            right_box_row, right_box_col = row - 1, col
            if not self._box_is_out_of_bounds(right_box_row, right_box_col):
                self._unassign_box(right_box_row, right_box_col)

    def edge_is_out_of_bounds(self, row, col):
        """Whether the coordinate is in the bounds of the board"""
        return row < 0 or row > self.row_bound or col < 0 or col > self.column_bound

    def is_edge(self, row, col):
        """Whether the coordinate corresponds to an edge"""
        return not self.is_even(row) == self.is_even(col)

    def is_player_one_box(self, row, col):
        """Whether the coordinate corresponds to a player one box coordinate"""
        return self.is_even(row) and self.is_even(col)

    def is_player_two_box(self, row, col):
        """Whether the coordinate corresponds to a player two box coordinate"""
        return not self.is_even(row) and not self.is_even(col)

    def is_horizontal_edge(self, row, col):
        """Whether the coordinate corresponds to a horizontal edge"""
        return self.is_even(row) and not self.is_even(col)

    def is_vertical_edge(self, row, col):
        """Whether the coordinate corresponds to a vertical edge"""
        return not self.is_even(row) and self.is_even(col)

    def taken(self, row, col):
        """PRE: (row, col) is a valid coordinate.
        Whether the box/edge is taken
        """
        return self.board[row][col]

    def game_over(self):
        """Whether the game is over"""
        return self._edges_remaining <= 0

    @property
    def rows(self):
        """Number of rows in the board"""
        return self._rows

    @property
    def columns(self):
        """Number of columns in the board"""
        return self._cols

    @property
    def row_bound(self):
        """Highest row index in matrix representation"""
        return 2 * self._rows

    @property
    def column_bound(self):
        """Highest column index in matrix representation"""
        return 2 * self._cols

    @property
    def player_one_score(self):
        """Player one's score"""
        return self._player_one_score

    @property
    def player_two_score(self):
        """Player two's score"""
        return self._player_two_score
    
    def _fill_edge(self, row, col):
        self.board[row][col] = True
        self._edges_remaining -= 1

    def _unfill_edge(self, row, col):
        self.board[row][col] = False
        self._edges_remaining += 1

    def _assign_box(self, row, col, player_one_turn):
        if player_one_turn:
            self.board[row][col] = True
            self._player_one_score += 1
        else:
            self.board[row + 1][col + 1] = True
            self._player_two_score += 1

    def _unassign_box(self, row, col):
        # player one won the box
        if self.board[row][col]:
            self.board[row][col] = False
            self._player_one_score -= 1
        # player two won the box
        if self.board[row + 1][col + 1]:
            self.board[row + 1][col + 1] = False
            self._player_two_score -= 1

    def _is_box_full(self, row, col):
        return (self.board[row][col + 1] and self.board[row + 2][col + 1]
            and self.board[row + 1][col] and self.board[row + 1][col + 2])

    def _box_is_out_of_bounds(self, row, col):
        return row < 0 or row > (self.row_bound - 2) or col < 0 or col > (self.column_bound - 2)

    @staticmethod
    def is_even(num):
        """PRE: num is an integer
        Whether num is even
        """
        return num % 2 == 0

