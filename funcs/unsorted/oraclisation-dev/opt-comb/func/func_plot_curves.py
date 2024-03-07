import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

def plot_curves(output_location, masks, mask_names, extra_masks, extra_mask_names):
    """
    Plots Averages, CoM and STD of each input and Combined Mask
    """
    fig, axs = plt.subplots(3, 2)
    
    c1 = 0
    c2 = 0
    for i in range(len(masks)):
        mask_plot = masks[i]/np.amax(masks[i])
        mask_plotter = []
        x = []
        mask_pos = []
        std = []
        x_og = np.linspace(0, 1, len(mask_plot))
        for ii in range(len(mask_plot)):
            CoM = ndimage.measurements.center_of_mass(mask_plot[ii])
            std.append(np.std(mask_plot[ii]))
            mask_pos.append(CoM[0]/4000)            
            mask_plotter.append(np.average(mask_plot[ii]))
            x.append(x_og[ii])
        axs[c1, c2].plot(x, mask_plotter, "o", mfc='none', label="Average of Row")
        if len(mask_pos) == len(mask_plotter):
            axs[c1, c2].plot(x, mask_pos, "o", mfc='none', label="Center of Mass of Row")
        if len(std) == len(mask_plotter):
            axs[c1, c2].plot(x, std, "o", mfc='none', label="Standard Deviation of Row")
        axs[c1, c2].set_title(mask_names[i])
        if c2 == 0:
            c2 += 1
        elif c2 == 1:
            c1 += 1
            c2 = 0

    for i in range(len(extra_masks)):
        mask_plot = extra_masks[i]/np.amax(extra_masks[i])

        mask_plotter = []
        x = []
        mask_pos = []
        std = []
        x_og = np.linspace(0, 1, len(mask_plot))
        for ii in range(len(mask_plot)):
            CoM = ndimage.measurements.center_of_mass(mask_plot[ii])
            std.append(np.std(mask_plot[ii]))
            mask_pos.append(CoM[0]/4000)
            mask_plotter.append(np.average(mask_plot[ii]))
            x.append(x_og[ii])
        
        axs[c1, c2].plot(x, mask_plotter, "o", mfc='none', label="Average of Row")
        if len(mask_pos) == len(mask_plotter):
            axs[c1, c2].plot(x, mask_pos, "o", mfc='none', label="Center of Mass of Row")
        if len(std) == len(mask_plotter):
            axs[c1, c2].plot(x, std, "o", mfc='none', label="Standard Deviation of Row")
        axs[c1, c2].set_title(extra_mask_names[i])
        if c2 == 0:
            c2 += 1
        elif c2 == 1:
            c1 += 1
            c2 = 0

    for ax in axs.flat:
        ax.set(xlabel='x-label', ylabel='y-label')

    for ax in axs.flat:
        ax.label_outer()
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

    fig.set_size_inches(20, 30)
    fig.legend()
    fig.savefig(output_location)