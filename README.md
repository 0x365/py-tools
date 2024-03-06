# PY-Tools
Python tools

### Matrix Reshape (matrix_reshape.py)
```python
coords, z = matrix_reshape_from_flat(grid_data, coord_dims, comp2d=True, plot_dims=[])
```

Inputs a matrix ```grid_data``` with dimensions M,N where there are N-1 coordinates given and 1 value at each coordinate. ```z``` output therefore has N-1 dimensions. Coords contains the corresponding values based on the input coordinates for each axis of ```z```.
