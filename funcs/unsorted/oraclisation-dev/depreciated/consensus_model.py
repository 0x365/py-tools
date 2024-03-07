from PIL import Image
import pathlib
import numpy as np
import PIL
import math
import matplotlib.pyplot as plt
import seaborn as sns

def my_std_2(point1, point2):
    avg = (point1 + point2)/2
    return math.sqrt( ( pow(point1-avg, 2) + pow(point2-avg, 2) )/2)

def my_std_3(point1, point2, point3):
    avg = (point1 + point2 + point3)/3
    return math.sqrt( ( pow(point1-avg, 2) + pow(point2-avg, 2) + pow(point3-avg, 2) )/3)

def get_image1():
    return np.random.rand(res,res)*255

def get_image2(in_grid):
    in_grid[in_grid > 200] = 0
    return in_grid
    #return np.random.rand(res,res)*255

res = 10
no = 2
runs = 1

std_li = []
weight_li = []



std_avg = 0

static1 = get_image1()
flat1 = static1.flatten()
static2 = get_image2(static1)
flat2 = static2.flatten()

std_sum = 0
for x in range(res):
    for y in range(res):
        std_sum += my_std_2(static1[x][y], static2[x][y])

std_avg += std_sum/pow(res,2)

std_li.append(std_avg/runs)
weight_li.append(1/10)
print("Done 1")

graph_file = str(pathlib.Path().resolve()) + "/src/data-small/graph"


# plt.plot(weight_li, std_li, marker="o", label=str(i))

# plt.ylabel('Avg Std')
# plt.xlabel('Weight_A (1 - Weight_B)')
sns.set()

# This is input 1
sns_plot = sns.kdeplot(data=flat1)
print(sns_plot)
fig = sns_plot.get_figure()

# This is input 2
sns_plot = sns.kdeplot(data=flat2)
fig = sns_plot.get_figure()

# This is output
flat3 = (flat1+flat2)/2
sns_plot = sns.kdeplot(data=flat3)
fig = sns_plot.get_figure()
fig.savefig(graph_file+".png")

print(flat1)
print(flat2)








# plt.legend()
# plt.savefig(graph_file)








# static_out = static1+static2

# # Outputs as image
# im = Image.fromarray(static_out, mode='L')
# path = str(pathlib.Path().resolve()) + "/src/data-small/output.tif"
# print(path)
# im.save(path)

