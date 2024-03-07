from PIL import Image
import os
import numpy as np
from numpy import savetxt, asarray
from matplotlib import pyplot as plt
import sys


sys.setrecursionlimit(10000)
#print(sys.getrecursionlimit())

#os.remove("data.csv")

Image.MAX_IMAGE_PIXELS = None

# Works for 3 but not 2 (1 is untested)
im = Image.open('image_in2.tif')


data = np.array(im)


xsize = data.shape[0]
ysize = data.shape[1]



print("Image X Size: ", xsize)
print("Image Y Size: ", ysize)
print()

for x in range(xsize):
    for y in range(ysize):
        if data[x][y] != 0:
            data[x][y] = 1

print(np.amax(data))

data2 = data

search_value = 1
change_colour = 5

plt.imshow(data2, interpolation='nearest')
plt.savefig('data.tif')



def find_start(data, search_value, start_coords):
    '''
    Function: Returns the first occurance of search_value in data
    Inputs: data (Numpy Array), search_value (Integer)
    Returns: found (Boolean), coords (Integer Tuple)
    '''
    x = start_coords[0]
    y = start_coords[1]
    xsize = data.shape[0]
    ysize = data.shape[1]
    still_search = 1
    found = 0
    coords = (0, 0)
    while still_search:
        if data[x][y] == search_value:
            still_search = 0
            found = 1
            coords = (x, y)
        x += 1
        if x == xsize:
            y += 1
            x = 0
        if x == xsize-1 and y == ysize-1:
            still_search = 0      
    return found, coords



def get_neighbours(coord):
    neighbours = []

    # May have to add edge detection

    neighbours.append((coord[0], coord[1]+1))
    neighbours.append((coord[0]+1, coord[1]))
    neighbours.append((coord[0]-1, coord[1]))
    neighbours.append((coord[0], coord[1]-1))

    return neighbours

def bfs(data, node):
    '''
    Function: Breadth first search of cells with same colour as input node that touch
    '''
    visited = []
    queue = []
    good_square = []

    search_value = data[node[0]][node[1]]

    good_square.append(node)
    visited.append(node)
    neighbours = get_neighbours(node)
    for neighbour in neighbours:
        if data[neighbour[0]][neighbour[1]] == search_value:
            queue.append(neighbour)

    count = 0
    while queue:
        s = queue.pop(0)

        neighbours = get_neighbours(s)
        for neighbour in neighbours:
            try:
                if neighbour not in visited and data[neighbour[0]][neighbour[1]] == search_value:
                    visited.append(neighbour)
                    queue.append(neighbour)
            except:
                continue
        good_square.append(s)
        count += 1
        if len(visited) > 4000:
            del visited[0:2000]
        if count % 10000 == 0:
            print("px",count)

        if count > 500000:
            # Force break for optimisation at 500k
            return good_square, count

    return good_square, count


print("Start")
coords = (0,0)
found = 1
counter = 0
all_cells = []
while found:
    found, coords = find_start(data2, search_value, coords)
    counter += 1
    print("--------------")
    print("Found")
    print(counter)
    if found:
        visited, count = bfs(data2, coords)
        all_cells.append(visited)
        for i in range(len(visited)):
            data2[visited[i][0]][visited[i][1]] = change_colour
        if count > 10000:
            plt.imshow(data2, interpolation='nearest')
            plt.savefig('data.tif')

plt.imshow(data2, interpolation='nearest')
plt.savefig('data.tif')

print("--------------------")
print("--------------------")
print("--------------------")
print("Segmenter finished")
print("--------------------")
print("--------------------")
print("--------------------")
print("Start searching for perimeter cells")


data = np.array(im)
for x in range(xsize):
    for y in range(ysize):
        if data[x][y] != 0:
            data[x][y] = 1

all_perimeter_cells = []
group_counter = 0
for group_cells in all_cells:
    print("------------")
    print("Group No:", group_counter)
    group_counter += 1
    perimeter_cells = []
    for cell in group_cells:
        neighbours = get_neighbours(cell)
        count = 0
        for neighbour in neighbours:
            try:
                #print(data[neighbour[0]][neighbour[1]])
                # I dont understand why this is change_colour, data does not get updated
                if data[neighbour[0]][neighbour[1]] != 1:
                    perimeter_cells.append(cell)
                    break
                    #count += 1
            except:
                print("error")
                continue
        #if count < 4:
            
            
    if perimeter_cells != []:
        all_perimeter_cells.append(perimeter_cells)

for perimeters in all_perimeter_cells:
    for cell in perimeters:
        data[cell[0]][cell[1]] = change_colour*2
plt.imshow(data, interpolation='nearest')
plt.savefig('perimeter_data.tif')


