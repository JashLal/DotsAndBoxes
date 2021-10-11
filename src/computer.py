class Computer:
    """
    Bot that utilizes a min-max search tree with finite depth to 
    determine the best move.
    """

    def __init__(self, backend):
        self._backend = backend

    def move(self):
        """Uses the min max algorithm to choose an edge. The depth of the
        algorithm is roughly based off the movespace size.
        """
        if self._backend._edges_remaining > 30:
            depth = 3
        elif self._backend._edges_remaining > 15:
            depth = 4
        elif self._backend._edges_remaining > 12:
            depth = 5
        elif self._backend._edges_remaining > 10:
            depth = 6
        else:
            depth = 7
        _, (row, col) = self._min_max(depth, True)
        return self._backend.move(row, col, False)

    def _min_max(self, depth, maximizer):
        """The min-max algorithm is a search tree that exhausts all moves
        per iteration recursing to the specified depth of the tree before
        evaluating the payoff of the move sequence.
        The algorithm accounts for alternating turns. It assumes the player
        plays optimally during their turn.
        The metric both the computer and user are optimizing is the difference
        in scores between the computer and user. The maximizer (computer)
        makes choices that maximizes this difference while the minimizer (player)
        makes chocies that minimizes this difference
        """
        if depth <= 0 or self._backend.game_over():
            return self._computer_advantage(), None
        # computer move
        if maximizer:
            max_advantage = float('-inf')
            optimal_move = None
            for row in range(self._backend.row_bound + 1):
                for col in range(self._backend.column_bound + 1):
                    if self._backend.is_edge(row, col) and not self._backend.taken(row, col):
                        same_turn = self._backend.move(row, col, False)
                        # box aquired --> maximizer; else --> minimizer
                        move_advantage, _ = self._min_max(depth - 1, same_turn)
                        if move_advantage > max_advantage:
                            max_advantage = move_advantage
                            optimal_move = (row, col)
                        # return to original state
                        self._backend.revert_move(row, col)
            return max_advantage, optimal_move
        # player move
        else:
            min_advantage = float('inf')
            optimal_move = None
            for row in range(self._backend.row_bound + 1):
                for col in range(self._backend.column_bound + 1):
                    if self._backend.is_edge(row, col) and not self._backend.taken(row, col):
                        same_turn = self._backend.move(row, col, True)
                        # box aquired --> minimizer; else --> maximizer
                        move_advantage, _ = self._min_max(depth - 1, not same_turn)
                        if move_advantage < min_advantage:
                            min_advantage = move_advantage
                            optimal_move = (row, col)
                        # return to original state
                        self._backend.revert_move(row, col)
            return min_advantage, optimal_move
           
    def _computer_advantage(self):
        return self._backend.player_two_score - self._backend.player_one_score