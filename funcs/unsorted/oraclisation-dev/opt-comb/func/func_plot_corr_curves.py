import matplotlib.pyplot as plt
import numpy as np
from func.func_rms_optimiser import corr_top, corr_bottom, get_rms

def plot_corr_curves(output_location, masks, mask_names):
    """
    Plot comparison of gov data vs dartmouth data... so on (Look for non-linear correlation across each comparison)
    """
    fig, axs = plt.subplots(len(masks), len(masks))

    c1 = 0
    c2 = 0
    corr_li = []
    rms_li = []
    for i in range(len(masks)):
        mask_plot_y = masks[i][1::20]
        mask_plot_y = mask_plot_y/np.amax(mask_plot_y)
        mask_plot_y = mask_plot_y.flatten()

        for ii in range(len(masks)):
            mask_plot_x = masks[ii][1::20]
            mask_plot_x = mask_plot_x/np.amax(mask_plot_x)
            mask_plot_x = mask_plot_x.flatten()    
        
            axs[c1, c2].plot(mask_plot_y, mask_plot_x, "o", mfc='none')#, mfc='none')
            corr = corr_top(mask_plot_y, mask_plot_x)/corr_bottom(mask_plot_y, mask_plot_x)
            rms = get_rms(mask_plot_y, mask_plot_x)
            if i == len(masks)-1:
                corr_li.append(corr)
                rms_li.append(rms)
            axs[c1, c2].set_title(str(i)+" vs "+str(ii)+" | Corr: "+str(round(corr,2))+" | RMS: "+str(round(rms,2)))

            if c2 < len(masks)-1:
                c2 += 1
            elif c2 == len(masks)-1:
                c1 += 1
                c2 = 0

            del mask_plot_x

    for ax in axs.flat:
        ax.set(xlabel='x-label', ylabel='y-label')

    for ax in axs.flat:
        ax.label_outer()
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

    fig.set_size_inches(30, 30)
    fig.savefig(output_location)
    return corr_li, rms_li