#this example  code is from Google AI Overveiw,  prompt: "networkx directed graph from a matrix"

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# 1. Define the adjacency matrix
# A = [[0, 1, 1],
#      [1, 0, 0],

#      [0, 1, 0]]
# Edges: (0 -> 1, weight 1), (0 -> 2, weight 1), (1 -> 0, weight 1), (2 -> 1, weight 1)
A = np.array([[0, 1, 1],
              [1, 0, 0],
              [0, 1, 0]])

# 2. Create the directed graph from the NumPy array
G = nx.from_numpy_array(A, create_using=nx.DiGraph())

# Optional: Print edges to verify
print("Edges of the graph:")
for edge in G.edges(data=True):
    print(edge)

# Optional: Draw the graph
# Using a specific layout for consistency in visualization
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black', arrows=True, connectionstyle='arc3, rad = 0.1')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
plt.title("Directed Graph from Adjacency Matrix")
plt.show()