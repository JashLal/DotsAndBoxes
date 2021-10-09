import unittest
from board import Board

class Computer:
    def __init__(self, backend):
        self.backend = backend

    def min_max(self, depth, maximizer):
        if depth == 0 or self.backend.game_over():
            return self._computer_advantage(), None
        # computer move
        if maximizer:
            max_advantage = float('-inf')
            optimal_move = None
            for row in range(self.backend.row_bound + 1):
                for col in range(self.backend.column_bound + 1):
                    row_is_even = row % 2 == 0
                    col_is_even = col % 2 == 0
                    # unfilled edge
                    if not row_is_even == col_is_even and not self.backend.edge_taken(row, col):
                        same_turn = self.backend.move(row, col, False)
                        # box aquired --> maximizer; else --> minimizer
                        move_advantage, _ = self.min_max(depth - 1, same_turn)
                        if move_advantage > max_advantage:
                            max_advantage = move_advantage
                            optimal_move = (row, col)
                        # return to original state
                        self.backend.revert_move(row, col)
            return max_advantage, optimal_move
        # user move
        else:
            min_advantage = float('inf')
            optimal_move = None
            for row in range(self.backend.row_bound + 1):
                for col in range(self.backend.column_bound + 1):
                    row_is_even = row % 2 == 0
                    col_is_even = col % 2 == 0
                    if not row_is_even == col_is_even and not self.backend.edge_taken(row, col):
                        same_turn = self.backend.move(row, col, True)
                        # box aquired --> minimizer; else --> maximizer
                        move_advantage, _ = self.min_max(depth - 1, not same_turn)
                        if move_advantage < min_advantage:
                            min_advantage = move_advantage
                            optimal_move = (row, col)
                        # return to original state
                        self.backend.revert_move(row, col)
            return min_advantage, optimal_move
           
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
        advantage, moves = computer.min_max(6, True)
        print(advantage)
        print(moves)
    
if __name__ == "__main__":
    unittest.main()