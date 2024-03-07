from osgeo import gdal
from scipy.optimize import minimize
from func.func_matrix_to_image import *
from func.func_rms_optimiser import *
from func.func_maps import *
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy import ndimage
from func.func_plot_curves import plot_curves
from func.func_plot_masks import plot_masks
from func.func_plot_corr_curves import plot_corr_curves


# Input image files
file_per_flood = r"/home/robert/oraclisation-dev/data/data-used/test_image.tif"
file_gov = r"/home/robert/oraclisation-dev/data/data-used/gov_working_test_image.tif"
file_google = r"/home/robert/oraclisation-dev/data/data-used/dartmout_observatory_output.tif"
file_global = r"/home/robert/oraclisation-dev/data/data-used/global_fl_database_flat.tif"
file_season = r"/home/robert/oraclisation-dev/data/data-used/seasonality_surface_water.tif" # Considered negative


# Get masks
mask_gov = get_source_easy(file_gov, [0, 0, 4000, 4000])
mask_per = get_source_easy(file_per_flood, [0, 0, 4000, 4000])
mask_glo = get_source_easy(file_global, [0, 0, 4000, 4000])


 # Create strange mask manually
src_goo = gdal.Open(file_google)
mask_goo, max_goo = get_mask(src_goo, [0, 0, 4000, 4000])
mask_goo[mask_goo == 0] = 10
mask_goo[mask_goo == 166] = 10
mask_goo[mask_goo == 208] = 10
mask_goo[mask_goo != 10] = 0
mask_goo = mask_goo * 255.0/10
del src_goo

 # Create strange mask manually
src_sea = gdal.Open(file_season)
mask_sea, max_sea = get_mask(src_sea, [0, 0, 4000, 4000])
mask_sea[mask_sea <= 1] = 0
mask_sea[mask_sea > 1] = 1
mask_sea[mask_sea == None] = 0
del src_sea



no = mask_gov.shape[0]*mask_gov.shape[1]

#mask_names = ["Global Flood Database Data", "Dartmouth Observatory Data", "Permenant Water Database Data", "Seasonal Water Database Data"]
#masks = [mask_glo, mask_goo, mask_per, mask_sea]

#mask_names = ["Government Data", "Global Flood Database Data", "Dartmouth Observatory Data", "Permenant Water Database Data", "Seasonal Water Database Data"]
#masks = [mask_gov, mask_glo, mask_goo, mask_per, mask_sea]

mask_names = ["Government Data", "Global Flood Database Data", "Dartmouth Observatory Data", "Permenant Water Database Data"]
masks = [mask_gov, mask_glo, mask_goo, mask_per]



# Remove permenant water
for i in range(len(masks)):
    masks[i] = masks[i]/np.amax(masks[i])
    masks[i] = masks[i] - mask_sea
    masks[i][masks[i] < 0] = 0



scaler = [0.0585456219985675, 0.7567792901377601, 0.028362655828507378, 0.15631243203516498]

if len(scaler) == len(masks):
    # Create combined
    for i in range(len(masks)):
        try:
            mask_comb = mask_comb + masks[i] * scaler[i]
        except:
            mask_comb = masks[i] * scaler[i]
else:
    for i in range(len(masks)):
        try:
            mask_comb = mask_comb + masks[i]
        except:
            mask_comb = masks[i]

extra_mask_names = ["Combined Masks"]
extra_masks = [mask_comb]



scale_mask_vis = 1

if scale_mask_vis:
    for i in range(len(masks)):
        masks[i] = masks[i] * scaler[i]



out_file = r"/home/robert/oraclisation-dev/data/data-out/plot_curves.png"
plot_curves(out_file, masks, mask_names, extra_masks, extra_mask_names)


out_file = r"/home/robert/oraclisation-dev/data/data-out/plot_masks.png"
plot_masks(out_file, masks, mask_names, extra_masks, extra_mask_names)


mask_names.append("Combined Mask")
masks.append(mask_comb)

out_file = r"/home/robert/oraclisation-dev/data/data-out/plot_corr_curves.png"
corr_li, rms_li = plot_corr_curves(out_file, masks, mask_names)

print()
print()
print("Final Data")
output_data = []
for i in range(len(mask_names)):
    output_data.append([mask_names[i], corr_li[i], rms_li[i]])


from tabulate import tabulate

print(tabulate(output_data, headers=["Mask Name", "Corr", "RMS"]))