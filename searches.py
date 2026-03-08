#this is sample code from a youtube video

import queue
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def order_bfs(graph, start_node):
    visited  =  set()
    q = queue.Queue()
    q.put(start_node)

    order = []

    while not q.empty():
        vertex = q.get()  #removes it
        if vertex not in visited:
            order.append(vertex)
            visited.add(vertex)
            for node in graph[vertex]:
                if node not in visited:
                    q.put(node) #adds next ones
                    #add nieghbors to q

    return order


def visualize_search(order, title, G, pos):
    plt.figure()
    plt.title(title)
    for i, node in enumerate(order, start=1):
        plt.clf()
        plt.title(title)
        nx.draw(G,pos,with_labels = True, node_color=['r' if  n==node  else 'g' for n in G.nodes])
        plt.draw()
        plt.pause(0.5)
    plt.show()
    time.sleep(0.5)




A = np.array([[0, 1, 1,1,0,1],
              [1, 0, 0,1, 0, 0],
              [0, 1, 0,0, 1, 0],
              [1, 0, 0,1, 0, 0],
              [0, 1, 0,1, 0, 0],
              [1, 0, 0,1, 0, 0]])

# 2. Create the directed graph from the NumPy array
G = nx.from_numpy_array(