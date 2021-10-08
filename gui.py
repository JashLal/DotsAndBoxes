from curses import wrapper
import curses
from board import Board

class Gui:
    OFFSET_X = 2
    OFFSET_Y = 2

    def __init__(self, backend):
        self.stdscr = curses.initscr()
        curses.noecho()
        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.backend = backend

    def _draw_board(self):
        for i in range(self.backend.row_bound + 1):
            for j in range(self.backend.column_bound + 1):
                row_is_even = i % 2 == 0
                col_is_even = j % 2 == 0
                if row_is_even and col_is_even:
                    self._draw_dot(i, j)
                    # user box
                    if self.backend.board[i][j]:
                        self._draw_box(i, j, True)
                elif row_is_even and not col_is_even and self.backend.board[i][j]:
                    self._draw_horizontal(i, j)
                elif not row_is_even and col_is_even and self.backend.board[i][j]:
                    self._draw_vertical(i, j)
                # computer box
                elif not row_is_even and not col_is_even and self.backend.board[i][j]:
                    self._draw_box(i - 1, j - 1, False)

    def move(self):
        row, col = 1, 0
        c = None
        # check compatibility in windows
        while not c == ord("\n") or self.backend.edge_taken(row, col):
            self._draw_board()
            self._draw_line(row, col)
            c = self.stdscr.getch()

            temp_row, temp_col = row, col
            if c == curses.KEY_UP:
                if temp_col < self.backend.column_bound:
                    temp_row -= 1
                    # alternate between horizontal and vertical
                    temp_col += (1 if temp_col % 2 == 0 else -1)
                else:
                    temp_row -= 2
            elif c == curses.KEY_DOWN:
                if temp_col < self.backend.column_bound:
                    temp_row += 1
                    # alternate between horizontal and vertical
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

        self.backend.move(row, col, True)
        self._draw_board()

    def _draw_dot(self, row, col):
        self.stdscr.addstr(self.OFFSET_Y + row, self.OFFSET_X + col * 2, "o")

    def _draw_line(self, row, col):
        row_is_even = row % 2 == 0
        # assuming coordinates are valid horizontal or vertical edges
        if row_is_even:
            self._draw_horizontal(row, col)
        else:
            self._draw_vertical(row, col)

    def _draw_horizontal(self, row, col):
        self.stdscr.addstr(self.OFFSET_Y + row, self.OFFSET_X + (col // 2) * 4 + 1, "---")

    def _draw_vertical(self, row, col):
        self.stdscr.addstr(self.OFFSET_Y + row, self.OFFSET_X + col * 2, "|")

    def _draw_box(self, row, col, user):
        self.stdscr.addstr(self.OFFSET_Y + row + 1, self.OFFSET_X + col * 2 + 2, "U" if user else "C")