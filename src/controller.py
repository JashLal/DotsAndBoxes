# -*- coding: utf-8 -*-
"""
Handles the Dots and Boxes game. Supports multiplayer and singleplayer.
"""

from board import Board
from gui import Gui
from computer import Computer
import curses
import argparse

class Controller:
    """Parses the command line and initializes the game objects."""
    def __init__(self):
        args = self._get_args()
        self.multiplayer = args.multiplayer
        self._backend = Board(args.cols, args.rows)
        self._display = Gui(self._backend)
        if not self.multiplayer:
            self._computer = Computer(self._backend)

    def _get_args(self):
        parser = argparse.ArgumentParser("To play Dots and Boxes, specify the board size " +
            "and whether you want to play singleplayer or multiplayer.")
        parser.add_argument('--rows', dest='rows', default=4, type=int, help="number of rows on the board")
        parser.add_argument('--cols', dest='cols', default=5, type=int, help="number of columns on the board")
        parser.add_argument('-m', dest='multiplayer', action='store_true', help='multiplayer mode (singleplayer if not present)')
        return parser.parse_args()

    def play_multiplayer(self):
        """Runs the game in multiplayer mode."""
        try:
            player_one_turn = True
            while not self._backend.game_over():
                same_turn = self._display.move(player_one_turn)
                if not same_turn:
                    player_one_turn = not player_one_turn
        except KeyboardInterrupt: 
            pass
        finally:
            curses.endwin()

    def play_singleplayer(self):
        """Runs the game in singleplayer mode."""
        try:
            player_turn = True
            while not self._backend.game_over():
                same_turn = False
                if player_turn:
                    same_turn = self._display.move(True)
                else:
                    same_turn = self._computer.move()
                if not same_turn:
                    player_turn = not player_turn
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

if __name__ == "__main__":
    controller = Controller()
    if controller.multiplayer:
        controller.play_multiplayer()
    else:
        controller.play_singleplayer()