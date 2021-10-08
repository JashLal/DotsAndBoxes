from curses import wrapper
import curses
from board import Board

OFFSET_X = 2
OFFSET_Y = 2

def main(stdscr):
    stdscr.clear()

    backend = Board()
    move(stdscr, backend)

def draw_board(stdscr, backend):
    for i in range(backend.row_bound + 1):
        for j in range(backend.column_bound + 1):
            row_is_even = i % 2 == 0
            col_is_even = j % 2 == 0
            if row_is_even and col_is_even:
                draw_dot(stdscr, i, j)
                # user box
                if backend.board[i][j]:
                    draw_box(stdscr, i, j, True)
            elif row_is_even and not col_is_even and backend.board[i][j]:
                draw_horizontal(stdscr, i, j)
            elif not row_is_even and col_is_even and backend.board[i][j]:
                draw_vertical(stdscr, i, j)
            # computer box
            elif not row_is_even and not col_is_even and backend.board[i][j]:
                draw_box(stdscr, i - 1, j - 1, False)

def move(stdscr, backend):
    row, col = 1, 0
    c = None
    # check compatibility in windows
    while not c == ord("\n") or backend.edge_taken(row, col):
        draw_board(stdscr, backend)
        draw_line(stdscr, row, col)
        stdscr.addstr(20, 2, f"({row}, {col})")
        stdscr.addstr(21, 2, f"{backend.column_bound}")
        c = stdscr.getch()

        temp_row, temp_col = row, col
        if c == curses.KEY_UP:
            if temp_col < backend.column_bound:
                temp_row -= 1
                # alternate between horizontal and vertical
                temp_col += (1 if temp_col % 2 == 0 else -1)
            else:
                temp_row -= 2
        elif c == curses.KEY_DOWN:
            if temp_col < backend.column_bound:
                temp_row += 1
                # alternate between horizontal and vertical
                temp_col += (1 if temp_col % 2 == 0 else -1)
            else:
                temp_row += 2
        elif c == curses.KEY_LEFT:
            if temp_row < backend.row_bound:
                temp_row += (1 if temp_row % 2 == 0 else -1)
                temp_col -= 1
            else:
                temp_col -= 2
        elif c == curses.KEY_RIGHT:
            if temp_row < backend.row_bound:
                temp_row += (1 if temp_row % 2 == 0 else -1)
                temp_col += 1
            else:
                temp_col += 2

        if not backend.edge_is_out_of_bounds(temp_row, temp_col):
           row, col = temp_row, temp_col 

        stdscr.clear()

    backend.move(row, col, True)
    draw_board(stdscr, backend)

def draw_dot(stdscr, row, col):
    stdscr.addstr(OFFSET_Y + row, OFFSET_X + col * 2, "o")

def draw_line(stdscr, row, col):
    row_is_even = row % 2 == 0
    # assuming coordinates are valid horizontal or vertical edges
    if row_is_even:
        draw_horizontal(stdscr, row, col)
    else:
        draw_vertical(stdscr, row, col)

def draw_horizontal(stdscr, row, col):
    stdscr.addstr(OFFSET_Y + row, OFFSET_X + (col // 2) * 4 + 1, "---")

def draw_vertical(stdscr, row, col):
    stdscr.addstr(OFFSET_Y + row, OFFSET_X + col * 2, "|")

def draw_box(stdscr, row, col, user):
    stdscr.addstr(OFFSET_Y + row + 1, OFFSET_X + col * 2 + 2, "U" if user else "C")

wrapper(main)