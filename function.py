import queue
import time
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import pygame

#PRE: board_size must be between 3 and 10
#POST: returns a matrix for the board that contains 30% blocked spots  
def create_board(board_size):
    board_matrix = np.zeros((board_size,board_size))
    total_spots = board_size * board_size

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

    #return result
    return board_matrix

#PRE:   board_size must be between 3 and 10
#       board_matrix must not be null
#POST:  returns a matrix where the  collumns and rows represent each board location
#       if the value in the cell is 1, there is a directted edge between those nodes 
#       if the value in the cell is 0, there is no edge between those nodes 

def create_graph_matrix(board_size, board_matrix):
    #   create a matrix with the rows and  collumns the length of the total amount of spots
    total_spots = board_size * board_size
    graph_matrix = np.zeros((total_spots,total_spots))


    #   look at each board space individually and identify it's neighbors 
    graph_index = 0 
    for i in range(board_size):
        for j in range(board_size):
            
            
            #   all indexes start as -1 unless a connection exists
            north_index = -1
            east_index = -1
            south_index = -1
            west_index =  -1


            #   if there exists a spot north
            if(i>0):
                north_index = board_matrix[i-1][j]
            
            #   if there exists a spot south
            if(i<board_size-1):
                south_index = board_matrix[i+1][j]
            
            #   if there exists a spot east
            if(j>0):
                east_index =  board_matrix[i][j-1]

            #   if there exists a spot west
            if(j<board_size-1):
                west_index =  board_matrix[i][j+1]

            #by the end, the current index has all it's neighboring connections

            #   if current spot isn't 1 (blocked)  or -1 (non-existant)
            if(board_matrix[i][j] == 0):

                #   fill graph matrix with 1 where there is a directed connection 
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

    return graph_matrix


#PRE:   option must be either "Player" or "Goal"
#       board_size must be between 3 and 10
#       board_matrix must not be null
#POST:  if  option is invalid, return -1
#       otherwise it sets a random open board spot to be the player or goal
#       and it returns the location of that spot in the graph
def set_random_node(option, board_size, board_matrix):
    
    #   check for invalid option input
    if(option != "Player" and option != "Goal" ):
        return -1

    #   pick random location
    #index_x = random.randint(0, board_size-1)
    #index_y = random.randint(0, board_size-1)


    #   translate the location from matrix to graph
    graph_location = -1
    found = False
    while(not found):
        #   picks random spot
        index_x = random.randint(0, board_size-1)
        index_y = random.randint(0, board_size-1)
        
        #   checks that random location isn't blocked
        if(board_matrix[index_x][index_y] == 0):
            
            #   sets player or goal location on the board matrix
            if(option == "Player"):
                board_matrix[index_x][index_y] = 2    #2 for player
            elif(option == "Goal"):
                board_matrix[index_x][index_y] = 3    #3 for goal
            
            #   sets player or goal location on the graph matrix
            graph_location = board_size*index_x + index_y
            
            #end loop
            found = True
            
    #returns the player or goal location on the graph
    return graph_location


#find the order that the agent searches 
def order_bfs(graph, start_node):
    visited  =  set()
    q = queue.Queue()
    q.put(start_node)

    order = []

    while not q.empty():
        vertex = q.get()
        if vertex not in visited:
            order.append(vertex)
            print(order)
            visited.add(vertex)
            for node in graph[vertex]:
                if node not in visited:
                    q.put(node)

    return order




#visualize the search
def visualize_search(order, title, G, pos, goal):
    count = 0
    plt.figure()
    plt.title(title)
    for i, node in enumerate(order, start=1):
        count = count+1
        if node == goal:
            print(count)
            return
        plt.clf()
        plt.title(title)
        nx.draw(G,pos,with_labels = True, node_color=['r' if  n==node or n==goal else 'g' for n in G.nodes])
        plt.draw()
        plt.pause(0.5)

    plt.show()
    time.sleep(0.5)


def visualize_board(board_matrix):

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
        #Draws a rectangle at specified screen coordinates.
        pygame.draw.rect(screen, color, [x, y, GRID_NODE_WIDTH, GRID_NODE_HEIGHT])

    # 5. Function to visualize the entire matrix
    def visualize_grid():
        #Iterates through the matrix and draws squares based on values.
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


    pygame.quit()


#support funuciton for  vvisualize in pygame 
def insert_visted_to_graph(visited, board_size,board_matrix, number):
    y = visited % board_size
    x = (visited  - y)/board_size

    board_matrix[int(x)][y] = number

#PRE:   board_matrix must not be null
#       board_size must be between 3 and 10
#       order must not be empty
#       shortest path must not be empty
#POST:  runs the animation of the agent on the board searching for the goal  
def visualize_in_pygame(board_matrix, board_size, order, shortest_path):

    pygame.init()

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    RED = (255,0,0)
    BLUE =  (0,0,255)
    LIGHT_BLUE =  (175,234,255)
    MID_BLUE =  (85, 154, 255)


    #size of one space
    GRID_NODE_WIDTH = 50
    GRID_NODE_HEIGHT = 50

    # Calculate screen size based on matrix dimensions and node size
    SCREEN_WIDTH = len(board_matrix[0]) * GRID_NODE_WIDTH
    SCREEN_HEIGHT = len(board_matrix) * GRID_NODE_HEIGHT

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BFS Search Visualization")

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
                if item == 0:   # 0 =  empty spot
                    create_square(x, y, WHITE)
                elif item == 1: # 1 = blocked spot
                    create_square(x, y, BLACK)
                elif item == 2:  # 2 =  player's start
                    create_square(x, y, BLUE)
                elif item == 3: # 3 = player's goal
                    create_square(x, y, RED)
                elif item == 4: # 4 = spots that have been seen
                    create_square(x, y, LIGHT_BLUE)
                elif item == 5: # 5 = spots in the shortest path
                    create_square(x, y, MID_BLUE)
                x += GRID_NODE_WIDTH  # move one "step" to the right
            y += GRID_NODE_HEIGHT  # move one "step" downwards


    running = True
    #i will iterate through the arrays order and shorest_path
    i = 0

    #phase1 being true   means  it will animate board's visible  spots in order
    #when phase1 is false, it will animate just  the boards shotst_path spots 
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

        #set visible spots ttoo light blue as they become visiblee
        if(phase1):
            insert_visted_to_graph(order[i],board_size, board_matrix,4)
            if (i<len(order)-1):
                i = i+1
        #set sport to mid blue as they become visited
        else:
            insert_visted_to_graph(shortest_path[i],board_size, board_matrix,5)
            if (i<len(shortest_path)-1):
                i = i+1

        #check for when the phase is over
        if(i == len(order)-1 ):
            i=0
            phase1 = False

        # Update the display
        pygame.display.update()

    pygame.quit()


