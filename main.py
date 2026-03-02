import numpy as np
import random

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
    print("rand = ", blocked_spot)

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
 
graph_matrix = np.zeros((open_spots_count,open_spots_count))


north_index = -1
east_index = -1
south_index = -1
west_index =  -1

for i in range(board_size):
    for j in range(board_size):
        #if theres a spot north
        if(i>0):
            north_index = board_matrix[i-1][j]
            print("(",i,",",j,") - N", north_index)
            #if index is 0, there is  a direction north
        
        #if theres a spot south
        if(i<board_size-1):
            south_index = board_matrix[i+1][j]
            print("(",i,",",j,") - S", south_index)
            #if index is 0, there is  a direction south
        
        #if theres a spot east
        if(j>0):
            east_index =  board_matrix[i][j-1]
            print("(",i,",",j,") - E", east_index)
            #if index is 0, there is  a direction east

        #if theres a spot west
        if(j<board_size-1):
            west_index =  board_matrix[i][j+1]
            print("(",i,",",j,") - W", west_index)
            #if index is 0, there is  a direction westt

print(graph_matrix)




