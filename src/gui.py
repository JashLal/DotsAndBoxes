# -*- coding: utf-8 -*-
"""
Terminal based GUI operating on the curses library.
Adapted from stephenroller's Dots and Boxes game https://gist.github.com/stephenroller/3163995.
"""

import curses

class Gui:
    """GUI for the Dots and Boxes game. Supports multiplayer mode; however, it is
    primarily used to implement and test the computer algorithms. 
    """

    # padding between terminal edges
    _OFFSET_X = _OFFSET_Y = 2
    # color classes
    _YELLOW_BLACK = 1
    _BLUE_BLACK = 2
    _BLACK_RED = 3

    def __init__(self, backend):
        # curses initialization
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.start_color()
        curses.init_pair(self._YELLOW_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(self._BLUE_BLACK, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(self._BLACK_RED, curses.COLOR_BLACK, curses.COLOR_RED)
        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.backend = backend

    def move(self, is_player_one):
        """Handles a player's move in the GUI. Updates the backend with
        the player's chosen move.
        Returns: Whether a box was aquired due to the move
        """
        row, col = 1, 0
        c = None
        # allows player to maneuver through board edges
        while not c == ord("\n") or self.backend.taken(row, col):
            self._draw_board()
            # red background line for invalid selection
            if self.backend.taken(row, col):
                self._draw_line(row, col, self._BLACK_RED)
            else:
                self._draw_line(row, col, self._determine_color(is_player_one))
            c = self.stdscr.getch()

            # handle arrow inputs
            # alternates between rows and columns while traversing in each
            # cardinal direction
            temp_row, temp_col = row, col
            if c == curses.KEY_UP:
                if temp_col < self.backend.column_bound:
                    temp_row -= 1
                    temp_col += (1 if temp_col % 2 == 0 else -1)
                else:
                    temp_row -= 2
            elif c == curses.KEY_DOWN:
                if temp_col < self.backend.column_bound:
                    temp_row += 1
                    temp_col += (1 if temp_col % 2 == 0 else -1)
                else:
                    temp_row += 2
            elif c == curses.KEY_LEFT:
                if temp_row < self.backend.row_bound:
                    temp_row += (1 if temp_row % 2 == 0 else -1)
                    temp_col -= 1
                else:
                    temp_col -= 2
            elif c == curses.KEY_RIGHT:
                if temp_row < self.backend.row_bound:
                    temp_row += (1 if temp_row % 2 == 0 else -1)
                    temp_col += 1
                else:
                    temp_col += 2

            if not self.backend.edge_is_out_of_bounds(temp_row, temp_col):
                row, col = temp_row, temp_col 

            self.stdscr.clear()

        # make move; keep track of whether box was aquired
        box_drawn = self.backend.move(row, col, is_player_one)
        self._draw_board()
        return box_drawn

    def _draw_board(self):
        for row in range(self.backend.row_bound + 1):
            for col in range(self.backend.column_bound + 1):
                if self.backend.is_player_one_box(row, col):
                    self._draw_dot(row, col)
                    if self.backend.taken(row, col):
                        self._draw_box(row, col, True)
                elif self.backend.is_horizontal_edge(row, col) and self.backend.taken(row, col):
                    self._draw_horizontal(row, col)
                elif self.backend.is_vertical_edge(row, col) and self.backend.taken(row, col):
                    self._draw_vertical(row, col)
                elif self.backend.is_player_two_box(row, col) and self.backend.taken(row, col):
                    self._draw_box(row - 1, col - 1, False)

    def _draw_dot(self, row, col):
        self.stdscr.addstr(self._OFFSET_Y + row, self._OFFSET_X + col * 2, "o")

    def _draw_line(self, row, col, color=0):
        if self.backend.is_horizontal_edge(row, col):
            self._draw_horizontal(row, col, color)
        else:
            self._draw_vertical(row, col, color)

    def _draw_horizontal(self, row, col, color=0):
        self.stdscr.addstr(self._OFFSET_Y + row, self._OFFSET_X + (col // 2) * 4 + 1, "---", curses.color_pair(color))

    def _draw_vertical(self, row, col, color=0):
        self.stdscr.addstr(self._OFFSET_Y + row, self._OFFSET_X + col * 2, "|", curses.color_pair(color))

    def _draw_box(self, row, col, is_player_one):
        self.stdscr.addstr(self._OFFSET_Y + row + 1, self._OFFSET_X + col * 2 + 2, "U" if is_player_one else "C", curses.color_pair(self._determine_color(is_player_one)))

    def _determine_color(self, is_player_one):
        return self._YELLOW_BLACK if is_player_one else self._BLUE_BLACK