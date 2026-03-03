#this example  code is from Google AI Overveiw,  prompt: "pygame representing a matrix example"


import pygame

# 1. Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# 2. Define the matrix (list of lists)
# 1s represent black squares, 0s represent white squares
matrix = [
    [1, 1, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 1]
]

# 3. Set up display and grid parameters
GRID_NODE_WIDTH = 50
GRID_NODE_HEIGHT = 50
# Calculate screen size based on matrix dimensions and node size
SCREEN_WIDTH = (len(matrix[0]) * GRID_NODE_WIDTH)*2
SCREEN_HEIGHT = (len(matrix) * GRID_NODE_HEIGHT)*2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Matrix Visualization")

# 4. Function to draw a single square
def create_square(x, y, color):
    """Draws a rectangle at specified screen coordinates."""
    pygame.draw.rect(screen, color, [x, y, GRID_NODE_WIDTH, GRID_NODE_HEIGHT])

# 5. Function to visualize the entire matrix
def visualize_grid():
    """Iterates through the matrix and draws squares based on values."""
    y = 0  # start at the top of the screen
    for row in matrix:
        x = 0  # for every row, start at the left of the screen again
        for item in row:
            if item == 0:
                create_square(x, y, WHITE)
            elif item == 2:
                create_square(x, y, GRAY)
            else:
                create_square(x, y, BLACK)
            x += GRID_NODE_WIDTH  # move one "step" to the right
        y += GRID_NODE_HEIGHT  # move one "step" downwards

# 6. Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing
    screen.fill(GRAY) # Fill background
    visualize_grid() # Draw the grid
    
    # Update the display
    pygame.display.update()

# 7. Quit Pygame
pygame.quit()
