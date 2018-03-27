import time
import sys

__author__ = 'Maxim Dutkin (max@dutkin.ru)'

chess_size = 5
print_timeout = 0.3
CURSOR_UP_ONE = '\033[F'
CURSOR_UP_N = '\033[%sA'
CURSOR_DOWN_N = '\033[%sB'
ERASE_LINE = '\033[K'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
ON_BLACK = '\033[40m'
ON_RED = '\033[41m'
ON_GREEN = '\033[42m'
COLOR_OFF = '\033[0m'


class ChessBoard:
    def __init__(self, size):
        self.size = size
        self.board = [[False for x in range(size)] for y in range(size)]
        self.active = None
        self.print_board(initial_print=True)

    def print_board(self, initial_print=False, stats=()):
        if not initial_print:
            delete_last_lines(self.size)
        for i in range(self.size):
            if i == 0:
                print('%s        %s' % (self.__print_row(i), stats))
            else:
                print(self.__print_row(i))

    def __print_row(self, row_num):
        buf = self.__render_v_sep()
        for i, x in enumerate(self.board[row_num]):
            buf += self.__render_cell((row_num, i))
            if i != self.size - 1:
                buf += self.__render_v_sep()
        buf += self.__render_v_sep()
        return buf

    def set_active(self, pos: (int, int)):
        self.active = pos

    def visit_cell(self, pos: (int, int), tour_stats=()):
        self.board[pos[0]][pos[1]] = True
        self.print_board(stats=tour_stats)
        time.sleep(print_timeout)

    def unvisit_cell(self, pos: (int, int), tour_stats=()):
        self.board[pos[0]][pos[1]] = False
        self.print_board(stats=tour_stats)

    def __render_cell(self, pos: (int, int)):
        return self.__render_visited(pos) if self.board[pos[0]][pos[1]] else self.__render_not_visited(pos)

    def __render_visited(self, pos: (int, int)):
        if self.active and self.active == pos:
            return GREEN + 'X' + COLOR_OFF
        else:
            return BLUE + 'X' + COLOR_OFF

    def __render_not_visited(self, pos: (int, int)):
        if self.active and self.active == pos:
            return ' '
        else:
            return ' '

    def __render_h_sep(self):
        return '--' * self.size

    def __render_v_sep(self):
        return '|'


def delete_last_lines(n=1):
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


def belongs_to_board(pos: (int, int)):
    """ checks if pos belongs to a board """
    return 0 <= pos[0] < chess_size and 0 <= pos[1] < chess_size


def moves_gen(pos: (int, int)):
    # shift ((x1, y1), (x2, y2), ...)
    possible_shifts = (
        (1, 2),
        (2, 1),
        (2, -1),
        (1, -2),
        (-1, -2),
        (-2, -1),
        (-2, 1),
        (-1, 2),
    )
    for shift in possible_shifts:
        possible_pos = (pos[0] + shift[0], pos[1] + shift[1])
        if belongs_to_board(possible_pos):
            yield possible_pos


board = ChessBoard(chess_size)


def find_tour(tour: list):
    cur_pos = tour[-1]
    for m in moves_gen(cur_pos):
        if m not in tour:
            tour.append(m)
            board.set_active(m)
            board.visit_cell(m, tour)
            if len(tour) == pow(chess_size, 2):
                return tour
            result = find_tour(tour)
            if not result:
                board.unvisit_cell(tour[-1], tour)
                tour.pop()
            else:
                return tour
        # else:
        #     continue
    return False


init_pos = (2, 2)
board.set_active(init_pos)
board.visit_cell(init_pos)
path = find_tour([init_pos, ])
print('path is unique: %s' % (len(path) == len(set(path))))
print('path: %s' % path)
