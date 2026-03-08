import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import queue

from function import* 


#create a matrix to represent the board  
    #0 = open sapce
    #1 = blocked space
    #2 = player's start position
    #3 = goal position

board_size = 5  #I've only  been ttesting number from 3 through 10
total_spots = board_size * board_size
board_matrix = create_board(board_size)

#prints board with 30% blocked spots
print(board_matrix)

#create a matrix that's compatible to the netwrokx  graph
graph_matrix = create_graph_matrix(board_size,board_matrix)

#set a random open spot in the board to be the player/goal positions, and returns the location of that spot in the graph
player_graph_location = set_random_node("Player",board_size,board_matrix )
goal_graph_location = set_random_node("Goal",board_size,board_matrix )


#prints board with 30% blocked spots and the player and goal on the board
print()
print(board_matrix)

#create the full board's connection graph with networkx
G = nx.from_numpy_array(graph_matrix, create_using=nx.DiGraph())
pos = nx.spring_layout(G)

#TESTING: uncomment these to visualize the graphing walking through a BFS and a pygame repsenation of the board's  start state

#visualize_search(order_bfs(G,player_graph_location), "title", G, pos, goal_graph_location)
#visualize_board(board_matrix)


#create a graph that represents only what the agent at the starting position can see
A = nx.Graph()
A.add_node(player_graph_location)

#   order will keep track of the order that spots are seen by the agent as it searches the board
order = []
#   current will be the node that  the player is at
current = player_graph_location
#   visible will keep track of all of the spots the agenntt has seen, but not visited yet
visible = queue.Queue()
#   start order at the starting spot
order.append(current)


#Add the starting position's nearest nodes to the graph before the loop begins
children = G.successors(current)
for i in list(children):
    visible.put(i)
    A.add_node(i)
    A.add_edge(current, i)
    order.append(i)

#continue to search the graph until all visble spots have been visited (or goal is found)
while(not visible.empty()):
    
    #   if the goal is now visible, end the loop
    if(goal_graph_location in visible.queue):
        
        #   add all the goal into the graph, and the order
        A.add_node(goal_graph_location)
        A.add_edge(current, goal_graph_location)
        order.append(goal_graph_location)
        
        #clear queue
        while not visible.empty():
            visible.get()
        
        #end loop
        break
    
    #   set the new visted node to the next visible spot in the queue (and remove that spot from the qeue)
    current = visible.get()


    #   add the current position's nearest nodes to the graph  and visible queue
    children = G.successors(current)
    for i in list(children):
        visible.put(i)
        A.add_node(i)
        A.add_edge(current, i)

        #   if the visible node hasn't already been seen, add it to the oroder, and use draw to keep track of this new graph state
        if(i not in order):
            order.append(i)
            nx.draw(A,pos,with_labels = True, node_color=['r' if  n==player_graph_location or n == goal_graph_location else 'g' for n in A.nodes])
            plt.draw()
            plt.pause(0.25)

#when all  spots have been visited or shortest path was  found,  use networkx library to get the shortest path
shortest_path = nx.shortest_path(A, source=player_graph_location, target=goal_graph_location)
print(shortest_path)

#this runs the animation for the graph at each of the drawn states
plt.show()
time.sleep(0.5)

#once the graph visialization is closed, run  the  board visualization
visualize_in_pygame(board_matrix, board_size, order, shortest_path)