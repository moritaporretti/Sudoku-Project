import random

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = 3
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return all(self.board[row][col] != num for row in range(self.row_length))

    def valid_in_box(self, row_start, col_start, num):
        for r in range(3):
            for c in range(3):
                if self.board[row_start + r][col_start + c] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row - row % 3, col - col % 3, num))

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        idx = 0
        for r in range(3):
            for c in range(3):
                self.board[row_start + r][col_start + c] = nums[idx]
                idx += 1

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_remaining(self, i, j):
        if i == self.row_length - 1 and j == self.row_length:
            return True
        if j == self.row_length:
            i += 1
            j = 0
        if i < self.box_length:
            if j < self.box_length:
                j = self.box_length
        elif i < self.row_length - self.box_length:
            if j == (i // self.box_length) * self.box_length:
                j += self.box_length
        else:
            if j == self.row_length - self.box_length:
                i += 1
                j = 0
                if i == self.row_length:
                    return True

        for num in range(1, 10):
            if self.is_valid(i, j, num):
                self.board[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)

    def remove_cells(self):
        count = 0
        while count < self.removed_cells:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count += 1

def generate_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    generator.fill_values()
    generator.remove_cells()
    return generator.get_board()

