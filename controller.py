from board import Board
from gui import Gui
import curses

backend = Board(2, 2)
frontend = Gui(backend)
try:
    player_one_turn = True
    while not backend.game_over():
        same_turn = frontend.move(player_one_turn)
        if not same_turn:
            player_one_turn = not player_one_turn
except KeyboardInterrupt:
    pass
finally:
    curses.endwin()