import matplotlib.pyplot as plt
import numpy as np
from matrix_sparsify import *

grid_data = np.round(10*np.random.rand(10,6))
print(np.array(grid_data,dtype=int))
coord_dims = [1,2,3,4,5]
# plot_dims = [2,3]
coords, z = sparse_to_dense(grid_data, coord_dims, comp2d=False)#, plot_dims=plot_dims)

# plt.contourf(coords[plot_dims[0]], coords[plot_dims[1]], z)
# plt.show()

print("INBETEWEEN")

# print(z)

print("INBETWEEN2")
sparse_again = dense_to_sparse(z, coords)

print(np.array(sparse_again, dtype=int))