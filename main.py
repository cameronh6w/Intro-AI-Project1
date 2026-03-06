import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import queue

from function import* 

#Board matrix with blocked paths
board_size = 10
total_spots = board_size * board_size

board_matrix = create_board(board_size)
print(board_matrix)


#   create a matrix that's compatible to the netwrokx  graph
graph_matrix = create_graph_matrix(board_size,board_matrix)

#will create a player and goal in the board and return the loction in the graph
player_graph_location = set_random_node("Player",board_size,board_matrix )
goal_graph_location = set_random_node("Goal",board_size,board_matrix )

print()
print(board_matrix)

#   output the graph with networkx
G = nx.from_numpy_array(graph_matrix, create_using=nx.DiGraph())
pos = nx.spring_layout(G)

#visualize_search(order_bfs(G,player_graph_location), "title", G, pos, goal_graph_location)

#visualize_board(board_matrix)


A = nx.Graph()
A.add_node(player_graph_location)

order = []

current = player_graph_location
visible = queue.Queue()
order.append(current)


print("node:",current)
children = G.successors(current)
for i in list(children):
    visible.put(i)
    #print("visible:",i)
    A.add_node(i)
    A.add_edge(current, i)
    order.append(i)


while(not visible.empty()):
    
    if(goal_graph_location in visible.queue):
        print("found")
        A.add_node(goal_graph_location)
        A.add_edge(current, goal_graph_location)
        order.append(goal_graph_location)
        #clear queue
        while not visible.empty():
            visible.get()
        break


    if(len(order) > total_spots):
        break
    
    current = visible.get()
    #print("node:",current)
    children = G.successors(current)
    for i in list(children):
        visible.put(i)
        #print("visible:",i)
        A.add_node(i)
        A.add_edge(current, i)
        if(i not in order):
            order.append(i)

shortest_path = nx.shortest_path(A, source=player_graph_location, target=goal_graph_location)

print(shortest_path)



"""visualize in pygame"""

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255,0,0)
BLUE =  (0,0,255)
LIGHT_BLUE =  (175,234,255)
MID_BLUE =  (85, 154, 255)


GRID_NODE_WIDTH = 50
GRID_NODE_HEIGHT = 50

# Calculate screen size based on matrix dimensions and node size
SCREEN_WIDTH = len(board_matrix[0]) * GRID_NODE_WIDTH
SCREEN_HEIGHT = len(board_matrix) * GRID_NODE_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Matrix Visualization")

# 4. Function to draw a single square
def create_square(x, y, color):
    #Draws a rectangle at specified screen coordinates.
    pygame.draw.rect(screen, color, [x, y, GRID_NODE_WIDTH, GRID_NODE_HEIGHT])

# 5. Function to visualize the entire matrix
def visualize_grid():
    #Iterates through the matrix and draws squares based on values.
    y = 0  # start at the top of the screen
    for row in board_matrix:
        x = 0  # for every row, start at the left of the screen again
        for item in row:
            if item == 0:   #
                create_square(x, y, WHITE)
            elif item == 1: #
                create_square(x, y, BLACK)
            elif item == 2:  #
                create_square(x, y, BLUE)
            elif item == 3: #
                create_square(x, y, RED)
            elif item == 4: #
                create_square(x, y, LIGHT_BLUE)
            elif item == 5: #
                create_square(x, y, MID_BLUE)
            x += GRID_NODE_WIDTH  # move one "step" to the right
        y += GRID_NODE_HEIGHT  # move one "step" downwards


running = True
i = 0
phase1= True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing
    screen.fill(GRAY) # Fill background

    visualize_grid() # Draw the grid
    time.sleep(0.05)

    if(phase1):
        insert_visted_to_graph(order[i],board_size, board_matrix,4)
        if (i<len(order)-1):
            i = i+1
    else:
        insert_visted_to_graph(shortest_path[i],board_size, board_matrix,5)
        if (i<len(shortest_path)-1):
            i = i+1

    
    
    if(i == len(order)-1 ):
        i=0
        phase1 = False


   
    # Update the display
    pygame.display.update()



pygame.quit()

