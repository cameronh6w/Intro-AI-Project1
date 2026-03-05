import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from function import* 

#Board matrix with blocked paths
board_size = 5
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
