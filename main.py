import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import pygame


#PHASE 1: Board matrix
board_size = 10
total_spots = board_size * board_size
board_matrix = np.zeros((board_size,board_size))

#PHASE 2: Obstacles 
#   decide how many spaces to block
percent_fill = int(total_spots * .333)


#   get a list of blocked spaces on the board 
blocked_spots = np.zeros(total_spots)
for i in range(percent_fill):
    blocked_spot = random.randint(0, total_spots-1)
    blocked_spots[blocked_spot] = 1


#   fill board with blocked spaces
b_index = 0
open_spots_count =0
for i in range(board_size):
    for j in range(board_size):
        if(blocked_spots[b_index]==1):
            board_matrix[i][j] = 1
        else:
            open_spots_count = open_spots_count+1
        b_index = b_index+1

print(board_matrix)

#PHASE 3: Connected Graph
#   create a matrix that's compatible to the netwrokx  graph
graph_matrix = np.zeros((total_spots,total_spots))




graph_index = 0 

#   look at each board space individually and identify it's neighbors 
for i in range(board_size):
    for j in range(board_size):
        
        
        #all indexes start as -1 unless a connection exists
        north_index = -1
        east_index = -1
        south_index = -1
        west_index =  -1


        #if there exists a spot north
        if(i>0):
            north_index = board_matrix[i-1][j]
        
        #if there exists a spot south
        if(i<board_size-1):
            south_index = board_matrix[i+1][j]
        
        #if there exists a spot east
        if(j>0):
            east_index =  board_matrix[i][j-1]

        #if there exists a spot west
        if(j<board_size-1):
            west_index =  board_matrix[i][j+1]

        #by the end, current index has it's all directions

        #if current spot isn't 1 (blocked)  or -1 non-existant
        if(board_matrix[i][j] == 0):

            #fill graph matrix with 1 where there is a directed connection 
            if(north_index == 0):
                graph_matrix[graph_index][graph_index-(board_size)] = 1
            if(east_index == 0):
                graph_matrix[graph_index][graph_index-1] = 1
            if(south_index == 0):
                graph_matrix[graph_index][graph_index+(board_size)] = 1
            if(west_index == 0):
                graph_matrix[graph_index][graph_index+1] = 1
            
        #increase index each time
        graph_index = graph_index+1
       

#   output the graph with networkx
G = nx.from_numpy_array(graph_matrix, create_using=nx.DiGraph())

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black', arrows=True, connectionstyle='arc3, rad = 0.1')
labels = nx.get_edge_attributes(G, 'weight')
#plt.show()

#PHASE 4: add player and goal
player_index_x = random.randint(0, board_size-1)
player_index_y = random.randint(0, board_size-1)
goal_index_x = random.randint(0, board_size-1)
goal_index_y = random.randint(0, board_size-1)

found = False
while(not found):
    player_index_x = random.randint(0, board_size-1)
    player_index_y = random.randint(0, board_size-1)
    if(board_matrix[player_index_x][player_index_y] != 1):
        board_matrix[player_index_x][player_index_y] = 2
        found = True

    
found = False
while(not found):
    goal_index_x = random.randint(0, board_size-1)
    goal_index_y = random.randint(0, board_size-1)
    
    if(board_matrix[goal_index_x][goal_index_y] != 1):
        board_matrix[goal_index_x][goal_index_y] = 3
        found = True

print()
print(board_matrix)



#PHASE 5: visualize 

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255,0,0)
BLUE =  (0,0,255)



GRID_NODE_WIDTH = 50
GRID_NODE_HEIGHT = 50

# Calculate screen size based on matrix dimensions and node size
SCREEN_WIDTH = len(board_matrix[0]) * GRID_NODE_WIDTH
SCREEN_HEIGHT = len(board_matrix) * GRID_NODE_HEIGHT

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
    for row in board_matrix:
        x = 0  # for every row, start at the left of the screen again
        for item in row:
            if item == 0:
                create_square(x, y, WHITE)
            elif item == 1:
                create_square(x, y, BLACK)
            elif item == 2:
                create_square(x, y, BLUE)
            elif item == 3:
                create_square(x, y, RED)
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


