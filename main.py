import numpy as np
import random


import networkx as nx
import matplotlib.pyplot as plt

#CREATE BOARD

board_size = 3
total_spots = board_size * board_size
board_matrix = np.zeros((board_size,board_size))

#decide how many spaces to block
percent_fill = int(total_spots * .333)
blocked_spots = np.zeros(total_spots)

print(board_matrix)
print(blocked_spots)

#get blocked spaces
for i in range(percent_fill):
    blocked_spot = random.randint(0, total_spots-1)
    #print("rand = ", blocked_spot)

    blocked_spots[blocked_spot] = 1

print(blocked_spots)

#fill board with blocked spaces
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

#create a matrix that's compatible to the netwrokx  graph
 
graph_matrix = np.zeros((total_spots,total_spots))


north_index = -1
east_index = -1
south_index = -1
west_index =  -1

graph_index = 0 
adjust = 0

for i in range(board_size):
    for j in range(board_size):
        north_index = -1
        east_index = -1
        south_index = -1
        west_index =  -1


        #if there exists a spot north
        if(i>0):
            north_index = board_matrix[i-1][j]
            #print("(",i,",",j,") - N", north_index)
            #if index is 0, there is  a direction north
        
        #if there exists a spot south
        if(i<board_size-1):
            south_index = board_matrix[i+1][j]
            #print("(",i,",",j,") - S", south_index)
            #if index is 0, there is  a direction south
        
        #if there exists a spot east
        if(j>0):
            east_index =  board_matrix[i][j-1]
            #print("(",i,",",j,") - E", east_index)
            #if index is 0, there is  a direction east

        #if there exists a spot west
        if(j<board_size-1):
            west_index =  board_matrix[i][j+1]
            #print("(",i,",",j,") - W", west_index)
            #if index is 0, there is  a direction westt

        #by the end, current index  has all directions
        #if current spot isn't 1 (blocked)
            #in  row 0, fill spots of th directions there are 
            #ie  (1,1)=4 w=current+1 s=((current + size) = 0+3 = 3 
                        # n = current-1

        if(board_matrix[i][j] == 0):
            if(north_index == 0):
                graph_matrix[graph_index][graph_index-(board_size)] = 1
            if(east_index == 0):
                graph_matrix[graph_index][graph_index-1] = 1
            if(south_index == 0):
                graph_matrix[graph_index][graph_index+(board_size)] = 1
            if(west_index == 0):
                graph_matrix[graph_index][graph_index+1] = 1
            
        graph_index =  graph_index+1
       

        
            
print()          
print("  0, 1, 2, 3, 4, 5, 6, 7, 8")
print(graph_matrix)
