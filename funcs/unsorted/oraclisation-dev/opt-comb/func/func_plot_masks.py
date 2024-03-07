import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage


def plot_masks(out_file, masks, mask_names, extra_masks, extra_mask_names):
    """
    Plots Input Masks and Combined Mask
    """
    fig2, axs2 = plt.subplots(3, 2)

    c1 = 0
    c2 = 0
    for i in range(len(masks)):
        mask_plot = masks[i]/np.amax(masks[i])
        axs2[c1, c2].imshow(mask_plot, interpolation='nearest')
        axs2[c1, c2].set_title(mask_names[i])
        if c2 == 0:
            c2 += 1
        elif c2 == 1:
            c1 += 1
            c2 = 0
    for i in range(len(extra_masks)):
        mask_plot = extra_masks[i]
        axs2[c1, c2].imshow(mask_plot, interpolation='nearest')
        axs2[c1, c2].set_title(extra_mask_names[i])
        if c2 == 0:
            c2 += 1
        elif c2 == 1:
            c1 += 1
            c2 = 0

    for ax in axs2.flat:
        ax.set(xlabel='Longitude (1 Degree/x pixels)', ylabel='Latitude (1 Degree/y pixels)')

    for ax in axs2.flat:
        ax.label_outer()

    fig2.set_size_inches(20, 30)
    fig2.savefig(out_file)