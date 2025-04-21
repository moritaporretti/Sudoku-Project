import pygame
import sys
from board_and_cell import Board

pygame.init()

WIDTH, HEIGHT = 540, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

def draw_buttons():
    easy_btn = pygame.Rect(50, 500, 120, 40)
    med_btn = pygame.Rect(210, 500, 120, 40)
    hard_btn = pygame.Rect(370, 500, 120, 40)

    pygame.draw.rect(screen, (200, 200, 200), easy_btn)
    pygame.draw.rect(screen, (200, 200, 200), med_btn)
    pygame.draw.rect(screen, (200, 200, 200), hard_btn)

    screen.blit(font.render("Easy", True, (0, 0, 0)), (85, 510))
    screen.blit(font.render("Medium", True, (0, 0, 0)), (230, 510))
    screen.blit(font.render("Hard", True, (0, 0, 0)), (405, 510))

    return easy_btn, med_btn, hard_btn

def draw_bottom_buttons():
    reset_btn = pygame.Rect(50, 550, 120, 40)
    restart_btn = pygame.Rect(210, 550, 120, 40)
    exit_btn = pygame.Rect(370, 550, 120, 40)

    pygame.draw.rect(screen, (200, 200, 200), reset_btn)
    pygame.draw.rect(screen, (200, 200, 200), restart_btn)
    pygame.draw.rect(screen, (200, 200, 200), exit_btn)

    screen.blit(font.render("Reset", True, (0, 0, 0)), (85, 560))
    screen.blit(font.render("Restart", True, (0, 0, 0)), (230, 560))
    screen.blit(font.render("Exit", True, (0, 0, 0)), (410, 560))

    return reset_btn, restart_btn, exit_btn

def draw_message(text):
    screen.fill((255, 255, 255))
    label = large_font.render(text, True, (0, 0, 0))
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(2000)

def start_screen():
    screen.fill((255, 255, 255))
    screen.blit(large_font.render("Select Difficulty", True, (0, 0, 0)), (150, 200))
    return draw_buttons()

def main():
    game_state = "start"
    board = None

    while True:
        if game_state == "start":
            easy_btn, med_btn, hard_btn = start_screen()

        elif game_state == "playing":
            screen.fill((255, 255, 255))
            board.draw()
            reset_btn, restart_btn, exit_btn = draw_bottom_buttons()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if easy_btn.collidepoint(x, y):
                        board = Board(WIDTH, HEIGHT, screen, "easy")
                        game_state = "playing"
                    elif med_btn.collidepoint(x, y):
                        board = Board(WIDTH, HEIGHT, screen, "medium")
                        game_state = "playing"
                    elif hard_btn.collidepoint(x, y):
                        board = Board(WIDTH, HEIGHT, screen, "hard")
                        game_state = "playing"

            elif game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < 540:
                        pos = board.click(x, y)
                        if pos:
                            board.select(*pos)
                    elif reset_btn.collidepoint(x, y):
                        board.reset_to_original()
                    elif restart_btn.collidepoint(x, y):
                        game_state = "start"
                    elif exit_btn.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.KEYDOWN and board.selected_cell:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        board.sketch(event.key - pygame.K_0)
                    elif event.key == pygame.K_RETURN:
                        board.place_number(board.selected_cell.sketched_value)
                        if board.is_full():
                            if board.check_board():
                                draw_message("You won!")
                            else:
                                draw_message("Incorrect solution")
                            game_state = "start"

if __name__ == "__main__":
    main()

