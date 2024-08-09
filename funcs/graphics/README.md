# Graphics
Python code a functions for copying into other programs.


## Pretty Matplotlib Plots with No Axis
```python
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,10),frameon=False)
plt.tight_layout()
ax = plt.Axes(fig, [0, 0, 1, 1])
ax.set_axis_off() # Modify with this off then turn on
fig.add_axes(ax)
# image is input numpy array
im = plt.imshow(image[:-500, 1000:-200], cmap="cividis", aspect='equal')
# Shrink changes size of colorbar, anchor moves it around
cbar = plt.colorbar(im, shrink=0.5, anchor=(-2,0.7))
cbar.set_label("Colorbar Label")
plt.savefig("image.png", dpi=1000, bbox_inches='tight')
```

## Other stuff
```python
# Invert y axis (or x axis)
plt.gca().invert_yaxis()

# Make space for tick markers
plt.tight_layout()
```
