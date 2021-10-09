from board import Board
from gui import Gui
from computer import Computer
import curses

backend = Board(2, 3)
frontend = Gui(backend)
computer = Computer(backend)
try:
    player_one_turn = True
    while not backend.game_over():
        same_turn = False
        # user turn
        if player_one_turn:
            same_turn = frontend.move(True)
        # computer turn
        else:
            if backend._edges_remaining > 30:
                _, (row, col) = computer.min_max(3, True)
            elif backend._edges_remaining > 15:
                _, (row, col) = computer.min_max(4, True)
            elif backend._edges_remaining > 12:
                _, (row, col) = computer.min_max(5, True)
            elif backend._edges_remaining > 10:
                _, (row, col) = computer.min_max(6, True)
            else:
                _, (row, col) = computer.min_max(7, True)
            same_turn = backend.move(row, col, False)
        if not same_turn:
            player_one_turn = not player_one_turn
except KeyboardInterrupt:
    pass
finally:
    curses.endwin()