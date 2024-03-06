import numpy as np
from itertools import product

def matrix_reshape_from_flat(grid_data, coord_dims ,comp2d=True, plot_dims=[]):

    grid_data = np.array(grid_data)

    unique_grid = np.asanyarray([np.unique(grid_data[:,i]) for i in coord_dims], dtype=object)

    dims = [len(unique_grid[i]) for i in range(len(unique_grid))]
    grid_other = np.zeros(dims, dtype=float)
    grid_other[grid_other == 0] = np.nan

    item_num = np.array(list(product(*[np.arange(dims[i]) for i in range(len(dims))])))
    permutations = np.array(list(product(*[unique_grid[i] for i in range(len(dims))])), dtype=tuple)

    indx = np.lexsort(np.rot90(permutations), axis=0)
    permutations = permutations[indx]
    item_num = item_num[indx]

    indx2 = np.lexsort(np.rot90(grid_data[:,coord_dims]), axis=0)
    grid_data = grid_data[indx2]
    grid_vals = grid_data[:,coord_dims]

    c = 0
    for i in range(len(grid_vals)):
        while (not np.all(grid_vals[i] == permutations[c])) and c < len(permutations)-1:
            c += 1
        if c == len(grid_vals)-1:
            break
        grid_other[tuple(item_num[c])] = grid_data[i, 0]

    if comp2d:
        mask = np.in1d(coord_dims, plot_dims)
        non_used = np.where(~mask)[0]
        compress_dims = np.array([coord_dims[i] for i in non_used])-1

        grid_other = np.nanmean(grid_other, axis=tuple(compress_dims))
    
    return unique_grid.tolist(), grid_other    