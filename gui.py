from curses import wrapper
from board import Board

OFFSET_X = 2
OFFSET_Y = 2

def main(stdscr):
    stdscr.clear()

    backend = Board()
    # backend.move(0, 1, True)
    # backend.move(1, 0, True)
    # backend.move(1, 8, True)
    # backend.move(10, 7, True)
    # backend.move(2, 1, True)
    # backend.move(1, 2, True)
    # backend.move(8, 7, True)
    # backend.move(9, 6, True)
    # backend.move(9, 8, False)
    draw_board(stdscr, backend)
    stdscr.refresh()
    while True:
        pass

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


def draw_dot(stdscr, row, col):
    stdscr.addstr(OFFSET_Y + row, OFFSET_X + col * 2, "o")

def draw_horizontal(stdscr, row, col):
    stdscr.addstr(OFFSET_Y + row, OFFSET_X + (col // 2) * 4 + 1, "---")

def draw_vertical(stdscr, row, col):
    stdscr.addstr(OFFSET_Y + row, OFFSET_X + col * 2, "|")

def draw_box(stdscr, row, col, user):
    stdscr.addstr(OFFSET_Y + row + 1, OFFSET_X + col * 2 + 2, "U" if user else "C")

wrapper(main)