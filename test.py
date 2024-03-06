import matplotlib.pyplot as plt
import numpy as np
from matrix_reshape import *

grid_data = np.round(10*np.random.rand(400,6))
coord_dims = [1,2,3,4,5]
plot_dims = [3,2]
coords, z = matrix_reshape_from_flat(grid_data, coord_dims, comp2d=True, plot_dims=plot_dims)

plt.contourf(coords[plot_dims[0]], coords[plot_dims[1]], z)
plt.show()