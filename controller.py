from board import Board
from gui import Gui
import curses

backend = Board()
frontend = Gui(backend)
try:
    user_turn = True
    while not backend.game_over():
        frontend.move()
except KeyboardInterrupt:
    pass
finally:
    curses.endwin()