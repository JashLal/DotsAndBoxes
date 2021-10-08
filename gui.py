from curses import wrapper
import curses
from board import Board

class Gui:
    OFFSET_X = 2
    OFFSET_Y = 2
    YELLOW_BLACK = 1
    BLUE_BLACK = 2
    BLACK_RED = 3

    def __init__(self, backend):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.start_color()
        curses.init_pair(self.YELLOW_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(self.BLUE_BLACK, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(self.BLACK_RED, curses.COLOR_BLACK, curses.COLOR_RED)
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

    def move(self, is_player_one):
        row, col = 1, 0
        c = None
        # check compatibility in windows
        while not c == ord("\n") or self.backend.edge_taken(row, col):
            self._draw_board()
            self._draw_line(row, col, self._determine_color(is_player_one))
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

        box_drawn = self.backend.move(row, col, is_player_one)
        self._draw_board()
        return box_drawn

    def _draw_dot(self, row, col):
        self.stdscr.addstr(self.OFFSET_Y + row, self.OFFSET_X + col * 2, "o")

    def _draw_line(self, row, col, color=0):
        row_is_even = row % 2 == 0
        # assuming coordinates are valid horizontal or vertical edges
        if row_is_even:
            self._draw_horizontal(row, col, color)
        else:
            self._draw_vertical(row, col, color)

    def _draw_horizontal(self, row, col, color=0):
        self.stdscr.addstr(self.OFFSET_Y + row, self.OFFSET_X + (col // 2) * 4 + 1, "---", curses.color_pair(color))

    def _draw_vertical(self, row, col, color=0):
        self.stdscr.addstr(self.OFFSET_Y + row, self.OFFSET_X + col * 2, "|", curses.color_pair(color))

    def _draw_box(self, row, col, is_player_one):
        self.stdscr.addstr(self.OFFSET_Y + row + 1, self.OFFSET_X + col * 2 + 2, "U" if is_player_one else "C", curses.color_pair(self._determine_color(is_player_one)))

    def _determine_color(self, is_player_one):
        return self.YELLOW_BLACK if is_player_one else self.BLUE_BLACK