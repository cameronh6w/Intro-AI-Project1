import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import queue

from function import* 

#Board matrix with blocked paths
board_size = 3
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

visualize_search(order_bfs(G,player_graph_location), "title", G, pos, goal_graph_location)

#visualize_board(board_matrix)



"""

#agent's visibilisty graph 
A = nx.Graph()
A.add_node(player_graph_location)

current = player_graph_location
next = queue.Queue()

print("goal:", goal_graph_location)

visited  = []
visited.append(player_graph_location)

while (True):
    
    if (current == goal_graph_location):
        break


    print ("qeue:",next.qsize())
    if next.empty():
        for i in list(G.successors(current)):
            if(i not in visited):
                A.add_node(i)
                A.add_edge(current,i)
                next.put(i)
    else:
       current = next.get()
       print ("qeue:", next.qsize())
       
    
    visited.append(current)
    print("Curent:", current)
    
    nx.draw(A,pos,with_labels = True, node_color=['r'])
    plt.draw()
    plt.pause(0.5)





#print(order_bfs(G,player_graph_location))

nx.draw(A,pos,with_labels = True, node_color=['r'])
plt.show()



#visualize_search(order_bfs(G,player_graph_location), "title", G, pos, goal_graph_location)

#visualize_board(board_matrix)


"""