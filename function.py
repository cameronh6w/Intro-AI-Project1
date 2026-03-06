import queue
import time
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import pygame

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



def create_graph_matrix(board_size, board_matrix):
    #   create a matrix that's compatible to the netwrokx  graph
    total_spots = board_size * board_size
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
    print(graph_matrix)
    return graph_matrix


def set_random_node(option, board_size, board_matrix):
    if(option != "Player" and option != "Goal" ):
        return -1


    index_x = random.randint(0, board_size-1)
    index_y = random.randint(0, board_size-1)


    #will translate the location from matrix to graph
    graph_location = -1

    found = False
    while(not found):
        #picks random spot
        index_x = random.randint(0, board_size-1)
        index_y = random.randint(0, board_size-1)
        
        #checks if random location is  blocked
        if(board_matrix[index_x][index_y] == 0):
            
            #sets player location for board  and graph
            if(option == "Player"):
                board_matrix[index_x][index_y] = 2    #2 for player
            elif(option == "Goal"):
                board_matrix[index_x][index_y] = 3    #3 for goal
            
            graph_location = board_size*index_x + index_y
            
            #end loop
            found = True

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

