import pygame
import random
import sys

from algorithms import manhattan_distance, solve_astar, heuristic, greedy_search


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (205, 55, 55)
GREEN = (252, 213, 60)
BLUE = (136, 213, 213)


pygame.init()

# Set the dimensions of the game window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cohesion")

# Define the game clock
clock = pygame.time.Clock()

# Set the size of each square on the board
SQUARE_SIZE = 100

# Define the width of the lines between squares
LINE_WIDTH = 2

#Define the total moves
moves = 0

#Define the position of the selected square
selected_row = None
selected_col = None
state = "menu"
def main_menu(screen):
    font = pygame.font.SysFont(None, 30)
    cohesion_text = font.render("C O H E S I O N", True, WHITE)
    play_text = font.render("PLAY", True, GREEN)
    credits_text = font.render("CREDITS", True, BLUE)
    exit_text = font.render("EXIT", True, RED)

    while True:
        screen.fill(BLACK)
        cohesion_rect = cohesion_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150))
        play_rect = play_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT / 2 + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_rect.collidepoint(x, y):
                    return 1

                elif credits_rect.collidepoint(x, y):
                    return 2
                elif exit_rect.collidepoint(x, y):
                    pygame.quit()
        screen.blit(cohesion_text, cohesion_rect)
        screen.blit(play_text, play_rect)
        screen.blit(credits_text, credits_rect)
        screen.blit(exit_text, exit_rect)
        pygame.display.flip()
        clock.tick(60)


def select_level(screen):
    font = pygame.font.SysFont(None, 40)
    easy_text = font.render("Easy", True, GREEN)
    medium_text = font.render("Medium", True, BLUE)
    hard_text = font.render("Hard", True, RED)

    while True:
        screen.fill(BLACK)
        easy_rect = easy_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        medium_rect = medium_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        hard_rect = hard_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if easy_rect.collidepoint(x, y):
                    return 1
                elif medium_rect.collidepoint(x, y):
                    return 2
                elif hard_rect.collidepoint(x, y):
                    return 3
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)
        pygame.display.flip()
        clock.tick(60)

def generate_board(level):
    red_squares = 0
    yellow_squares = 0
    blue_squares = 0
    color_counts = {1: 6, 2: 9, 3: 13}
    num_colored = color_counts.get(level, 0)
    board = [[0] * 4 for _ in range(4)]
    while num_colored > 0:
        row, col = random.randint(0, 3), random.randint(0, 3)
        if board[row][col] == 0:
            board[row][col] = random.choice([1, 2, 3])
            if board[row][col] == 1:
                red_squares += 1
            elif board[row][col] == 2:
                yellow_squares +=1
            elif board[row][col] == 3:
                blue_squares += 1
            num_colored -= 1
    return board

def handle_events(board, selected_square):
    global moves
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row = mouse_y // SQUARE_SIZE
            col = mouse_x // SQUARE_SIZE
            if len(selected_square) < 2:  # add this check
                if board[row][col] != 0:
                    selected_square[:] = [row, col]
            else:
                if board[row][col] == 0 and ((row == selected_square[0] and abs(col - selected_square[1]) == 1) or
                                             (col == selected_square[1] and abs(row - selected_square[0]) == 1)):
                    board[row][col] = board[selected_square[0]][selected_square[1]]
                    board[selected_square[0]][selected_square[1]] = 0
                    selected_square[:] = []
                    moves += 1
    return True, moves


def update_screen(screen, board):
    screen.fill(BLACK)
    for row in range(4):
        for col in range(4):
            square_color = WHITE
            if board[row][col] == 1:
                square_color = RED
            elif board[row][col] == 2:
                square_color = GREEN
            elif board[row][col] == 3:
                square_color = BLUE
            pygame.draw.rect(screen, square_color, [col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE])
            #pygame.draw.rect(screen, BLACK, [col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE], LINE_WIDTH)
    for i in range(1, 4):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (SCREEN_WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, SCREEN_HEIGHT), LINE_WIDTH)


def merge_cells(board):

    for row in range(4):
        for col in range(4):
            if board[row][col] != 0:
                # Check the cell to the right
                if col < 3 and board[row][col] == board[row][col + 1]:
                    color = get_color(board[row][col])
                    pygame.draw.line(screen, color, ((col + 1) * SQUARE_SIZE, (row) * SQUARE_SIZE),
                                     ((col + 1) * SQUARE_SIZE, (row) * SQUARE_SIZE + SQUARE_SIZE), LINE_WIDTH)
                    board[row][col + 1] = board[row][col]
                # Check the cell below
                if row < 3 and board[row][col] == board[row + 1][col]:
                    color = get_color(board[row][col])
                    pygame.draw.line(screen, color, ((col) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE),
                                     ((col) * SQUARE_SIZE + SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                    board[row + 1][col] = board[row][col]

def get_color(cell_value):
    if cell_value == 1:
        return RED
    elif cell_value == 2:
        return GREEN
    elif cell_value == 3:
        return BLUE


def check_win(board):
    colors = set([1, 2, 3])
    for color in colors:
        squares = []
        for row in range(4):
            for col in range(4):
                if board[row][col] == color:
                    squares.append((row, col))
        if len(squares) < 2:
            continue
        visited = set()
        stack = [squares[0]]
        while stack:
            row, col = stack.pop()
            visited.add((row, col))
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_row, new_col = row + dr, col + dc
                if (new_row, new_col) in squares and (new_row, new_col) not in visited:
                    stack.append((new_row, new_col))
        if len(visited) != len(squares):
            return False
    return True



def game(board):
    selected_square = []
    merged_cells = []
    running = True
    while running:

        running = handle_events(board, selected_square)
        update_screen(screen, board)
        merge_cells(board)
        if check_win(board):
            moves = handle_events(board, selected_square)
            moves_screen = pygame.display.set_mode((400, 400))
            pygame.display.set_caption("Puzzle Solved!")
            font = pygame.font.SysFont(None, 40)
            puzzle_solved_text = font.render("PUZZLE SOLVED!", True, BLUE)
            puzzle_solved_rect = puzzle_solved_text.get_rect(center=(200, 150))
            moves_text = font.render("Total moves: " + str(moves[1]), True, WHITE)
            moves_rect = moves_text.get_rect(center=(200, 300))
            moves_screen.fill(BLACK)
            moves_screen.blit(puzzle_solved_text, puzzle_solved_rect)
            moves_screen.blit(moves_text, moves_rect)
            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # The player clicked on the moves window
                        return
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cohesion")
    clock = pygame.time.Clock()
    state = main_menu(screen)
    if state == 1:
        level = select_level(screen)
        board = generate_board(level)
        path = greedy_search(board, heuristic)
        if path:
            print("solução greedy: ", len(path))
            for state,move in path:
                print(move, ":", state)
        path = solve_astar(board, heuristic)
        if path:
            print("solução A*: ", len(path))
            for state,move in path:
                print(move, ":", state)

    if state == 2:
        font = pygame.font.SysFont(None, 30)
        b_text = font.render("Benedita Gonçalves", True, WHITE)
        b_rect = b_text.get_rect(center=(200, 180))
        s_text = font.render("Sara Táboas", True, WHITE)
        s_rect = s_text.get_rect(center=(200, 220))
        screen.fill(BLACK)
        screen.blit(b_text, b_rect)
        screen.blit(s_text, s_rect)
        pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # The player clicked on the moves window
                return
        pygame.display.flip()
        clock.tick(60)

    game(board)
    pygame.quit()
    sys.exit()

main()

