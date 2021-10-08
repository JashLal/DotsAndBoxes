import unittest
from board import Board

class Computer:
    def __init__(self, backend):
        self.backend = backend

    def _min_max(self, depth, maximizer):
        if depth == 0:
            return self._computer_advantage()
        # computer move
        if maximizer:
            max_advantage = float('-inf')
            for row in range(self.backend.row_bound + 1):
                for col in range(self.backend.column_bound + 1):
                    row_is_even = row % 2 == 0
                    col_is_even = col % 2 == 0
                    # unfilled edge
                    if not row_is_even == col_is_even and not self.backend.edge_taken(row, col):
                        self.backend.move(row, col, maximizer)
                        move_advantage = self._min_max(depth - 1, not maximizer)
                        max_advantage = max(max_advantage, move_advantage)
                        # return to original state
                        self.backend.revert_move(row, col)
            return max_advantage
        # user move
        else:
            min_advantage = float('inf')
            for row in range(self.backend.row_bound + 1):
                for col in range(self.backend.column_bound + 1):
                    row_is_even = row % 2 == 0
                    col_is_even = col % 2 == 0
                    if not row_is_even == col_is_even and not self.backend.edge_taken(row, col):
                        self.backend.move(row, col, maximizer)
                        move_advantage = self._min_max(depth - 1, not maximizer)
                        min_advantage = min(min_advantage, move_advantage)
                        # return to original state
                        self.backend.revert_move(row, col)
            return min_advantage
           
    def _computer_advantage(self):
        return self.backend.player_two_score - self.backend.player_one_score

class Test(unittest.TestCase):
    def test_min_max(self):
        backend = Board(3, 3)
        computer = Computer(backend)
        backend.move(0, 1, True)
        backend.move(0, 3, True)
        backend.move(1, 0, True)
        backend.move(1, 4, True)
        backend.move(1, 6, True)
        backend.move(3, 0, True)
        backend.move(3, 2, True)
        backend.move(3, 4, True)
        backend.move(3, 6, True)
        backend.move(5, 0, True)
        backend.move(5, 4, True)
        backend.move(5, 6, True)
        backend.move(6, 1, True)
        backend.move(6, 3, True)
        print(computer._min_max(5, True))

if __name__ == "__main__":
    unittest.main()