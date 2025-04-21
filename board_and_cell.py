import pygame
from sudoku_generator import generate_sudoku

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False
        self.original = value != 0

    def set_cell_value(self, value):
        if not self.original:
            self.value = value

    def set_sketched_value(self, value):
        if not self.original:
            self.sketched_value = value

    def draw(self):
        font = pygame.font.Font(None, 40)
        x = self.col * 60
        y = self.row * 60
        rect = pygame.Rect(x, y, 60, 60)

        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)

        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + 20, y + 15))
        elif self.sketched_value != 0:
            text = font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected_cell = None

        removed = {"easy": 30, "medium": 40, "hard": 50}.get(difficulty, 30)

        self.original_board = generate_sudoku(9, removed)
        self.solved_board = [row[:] for row in self.original_board]
        self.cells = [[Cell(self.original_board[r][c], r, c, screen) for c in range(9)] for r in range(9)]

    def draw(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].draw()

        for i in range(10):
            width = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 60), (540, i * 60), width)
            pygame.draw.line(self.screen, (0, 0, 0), (i * 60, 0), (i * 60, 540), width)

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if 0 <= x < 540 and 0 <= y < 540:
            return y // 60, x // 60
        return None

    def clear(self):
        if self.selected_cell and not self.selected_cell.original:
            self.selected_cell.set_cell_value(0)
            self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.set_sketched_value(0)

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                if not cell.original:
                    cell.set_cell_value(0)
                    cell.set_sketched_value(0)

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def update_board(self):
        for r in range(9):
            for c in range(9):
                self.original_board[r][c] = self.cells[r][c].value

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return r, c
        return None

    def check_board(self):
        self.update_board()
        return self.original_board == self.solved_board
