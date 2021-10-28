import copy
import random
import numpy as np


class Board:
    def __init__(self):
        self.board = self.zero_board()

    # Returns zeroed 9x9 np array
    def zero_board(self):
        return np.zeros((9, 9))

    def find_empty_grid(self):
        (rows, cols) = np.where(self.board == 0)
        if rows.size == 0:
            return np.array([]), np.array([])
        return rows[0], cols[0]

    def check_insert_num(self, num, grid):
        row, col = grid
        if (not self.board[row][col] == 0) or (num in self.board[row, :]) or (num in self.board[:, col]):
            return False

        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3

        if num in self.board[box_row_start: box_row_start + 3, box_col_start: box_col_start + 3]:
            return False

        return True

    def solve(self):
        row, col = self.find_empty_grid()

        if row.size == 0:
            return True

        for n in range(1, 10):
            if self.check_insert_num(n, (row, col)):
                self.board[row][col] = n

                if self.solve():
                    return True
                self.board[row][col] = 0

        return False

    def fill_diag_block(self, index):
        _l = list(range(1, 10))
        for row in range(index, index + 3):
            for col in range(index, index + 3):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

    def gen_filled_board(self):
        self.zero_board()

        for i in range(0, 7, 3):
            self.fill_diag_block(i)

        return self.gen_recursive()

    def gen_recursive(self):
        row, col = self.find_empty_grid()
        if not row.size == 0:
            _num = random.randint(1, 9)

            if self.check_insert_num(_num, (row, col)):
                self.board[row][col] = _num

                a = Board()
                a.board = np.copy(self.board)

                if not a.solve():
                    self.board[row][col] = 0

            self.gen_recursive()

        return True

    def is_unique_sol(self):
        for row, col in np.ndindex(self.board.shape):
            if self.board[row, col] == 0:
                counter = 0
                for n in range(10):
                    if counter > 1:
                        return False
                    if self.check_insert_num(n, (row, col)):
                        self.board[row][col] = n
                        a = Board()
                        a.board = np.copy(self.board)
                        if a.solve():
                            counter += 1
                        self.board[row][col] = 0
        return True

    def gen_sudoku(self, difficulty=1):
        if difficulty not in [0, 1, 2]:
            raise ValueError("Enter number for difficulty\n0: simple\n1: normal\n2: hard")

        grids_to_remove = [36, 46, 52][difficulty]

        self.gen_filled_board()

        while grids_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if self.board[row][col] != 0:
                n = self.board[row][col]
                self.board[row][col] = 0

                if not self.is_unique_sol():
                    self.board[row][col] = n
                    continue

                grids_to_remove -= 1

        return self.board


if __name__ == '__main__':
    print('hello')

    # b = Board()
    #
    # completed = [[3, 9, 1, 2, 8, 6, 5, 7, 4],
    #              [4, 8, 7, 3, 5, 9, 1, 2, 6],
    #              [6, 5, 2, 7, 1, 4, 8, 3, 9],
    #              [8, 7, 5, 4, 3, 1, 6, 9, 2],
    #              [2, 1, 3, 9, 6, 7, 4, 8, 5],
    #              [9, 6, 4, 5, 2, 8, 7, 1, 3],
    #              [1, 4, 9, 6, 7, 3, 2, 5, 8],
    #              [5, 3, 8, 1, 4, 2, 9, 6, 7],
    #              [7, 2, 6, 8, 9, 5, 3, 4, 1]]
    #
    # b.board = np.array(completed)
    # print(b.board)
    #
    # b.board[1][5] = 0
    # b.board[7][4] = 0
    # b.board[8][1] = 0
    # print(b.board)
    #
    # b.solve()
    #
    # print(b.board)

    # a = Board()
    #
    # # a.gen_complete_board()
    # print(a.gen_complete_board())
    # print(a.board)


    # c = Board()
    #
    # not_uniqe = [[2, 9, 5, 7, 4, 3, 8, 6, 1],
    #              [4, 3, 1, 8, 6, 5, 9, 0, 0],
    #              [8, 7, 6, 1, 9, 2, 5, 4, 3],
    #              [3, 8, 7, 4, 5, 9, 2, 1, 6],
    #              [6, 1, 2, 3, 8, 7, 4, 9, 5],
    #              [5, 4, 9, 2, 1, 6, 7, 3, 8],
    #              [7, 6, 3, 5, 2, 4, 1, 8, 9],
    #              [9, 2, 8, 6, 7, 1, 3, 5, 4],
    #              [1, 5, 4, 9, 3, 8, 6, 0, 0]]
    #
    # c.board = np.array(not_uniqe)
    #
    # print(c.is_unique_sol())

    d = Board()

    d.gen_sudoku(0)

    print(d.board)

    d.solve()

    print(d.board)
