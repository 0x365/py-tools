import time

def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        return tempTimeInterval

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)


import math
import numpy as np

def my_std(point1, point2, point3):
    avg = (point1 + point2 + point3)/3
    return math.sqrt( ( pow(point1-avg, 2) + pow(point2-avg, 2) + pow(point3-avg, 2) )/3)

tests = 10000

print("Numpy Std")
timer = 0
for i in range(tests):
    tic()
    (np.std([3, 5, 10]))
    timer += toc()
avg_time1 = timer/tests
print("Time: ", avg_time1)

print("My Std")
timer = 0
for i in range(tests):
    tic()
    (my_std(3, 5, 10))
    timer += toc()
avg_time2 = timer/tests
print("Time: ", avg_time2)

print("Average amount faster: ", avg_time1/avg_time2)