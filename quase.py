import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (205, 55, 55)
GREEN = (252, 213, 60)
BLUE = (136, 213, 213)

# Initialize Pygame
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

# Define the board as a 2D array
board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

# Randomly assign colors to some squares on the board
for row in range(4):
    for col in range(4):
        if random.randint(0, 1) == 1:
            color = random.choice([1, 2, 3])
            board[row][col] = color

# Define the position of the selected square
selected_row = None
selected_col = None

# Create a loop to keep the game running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            row = mouse_y // SQUARE_SIZE
            col = mouse_x // SQUARE_SIZE
            if selected_row is None:
                if board[row][col] != 0:
                    selected_row = row
                    selected_col = col
            else:
                if board[row][col] == 0 and ((row == selected_row and abs(col - selected_col) == 1) or
                                             (col == selected_col and abs(row - selected_row) == 1)):
                    board[row][col] = board[selected_row][selected_col]
                    board[selected_row][selected_col] = 0
                    selected_row = None
                    selected_col = None

    # Fill the background with white
    screen.fill(WHITE)

    # Draw the squares and lines on the board
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
            pygame.draw.rect(screen, BLACK, [col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE], LINE_WIDTH)

    # Draw the lines between the squares
    for i in range(1, 4):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (SCREEN_WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, SCREEN_HEIGHT), LINE_WIDTH)

    # Update the display
    pygame.display.flip()

    # Set the game clock speed
    clock.tick(60)

