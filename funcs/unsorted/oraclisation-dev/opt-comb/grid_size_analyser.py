from osgeo import gdal
from scipy.optimize import minimize
from func.func_matrix_to_image import *
from func.func_rms_optimiser import *
from func.func_maps import *

# Input image files
file_per_flood = r"/home/robert/oraclisation-dev/data/data-used/test_image.tif"
file_gov = r"/home/robert/oraclisation-dev/data/data-used/gov_working_test_image.tif"
file_google = r"/home/robert/oraclisation-dev/data/data-used/dartmout_observatory_output.tif"
file_global = r"/home/robert/oraclisation-dev/data/data-used/global_fl_database_flat.tif"
file_season = r"/home/robert/oraclisation-dev/data/data-used/seasonality_surface_water.tif" # Considered negative

out_file = r"/home/robert/oraclisation-dev/src/output.tif"
out_file_data = r"/home/robert/oraclisation-dev/src/output_with_rivers.tif"

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
mask_sea[mask_sea > 1] = 999
mask_sea[mask_sea <= 1] = 0
mask_sea[mask_sea == None] = 0
del src_sea

wid = mask_gov.shape[0]
no = mask_gov.shape[0]*mask_gov.shape[1]


reset = 1       # Whether or not to generate new data or pull from file

mask_names = ["mask_gov", "mask_glo", "mask_goo", "mask_per"]
masks = [mask_gov, mask_glo, mask_goo, mask_per]

divisions = [1, 10]

masks2 = masks

for divider in divisions:
    if wid % divider != 0 or divider > wid:
        raise Exception("Divider is not correct size")

for mask in masks:
    mask = mask/np.amax(mask)

# Takes a slice
p_corr_li = []
mask_li = []
scaler_li = []
scaler_blank = [1, 1, 1, 1]
for divider in divisions:
    p_corr_avg = 0
    for i in range(0, wid, int(wid/divider)):
        masks_i = []
        for mask in masks:
            masks_i.append(mask[i:i+int(wid/divider)])


        scaler = run_minimize(masks_i, precision=1e-4) #mask_neg=mask_sea
        
        for ii in range(len(masks2)):
            masks2[ii][i:i+int(wid/divider)] = masks_i[ii]*scaler[ii]

    p_corr_avg += 1/all_corr(scaler_blank, masks2)
    p_corr_li.append(p_corr_avg)
    mask_li.append(masks2)
    scaler_li.append(scaler)

print(p_corr_li)

out_file1 = r"/home/robert/oraclisation-dev/src/output_blank.tif"
out_file2 = r"/home/robert/oraclisation-dev/src/output_div1.tif"
out_file3 = r"/home/robert/oraclisation-dev/src/output_div10.tif"

matrix_to_image_func(masks, scaler_blank, out_file1, matrix_neg=mask_sea)
matrix_to_image_func(mask_li[0], scaler_blank, out_file2, matrix_neg=mask_sea)
matrix_to_image_func(mask_li[1], scaler_blank, out_file3, matrix_neg=mask_sea)




# # Decide whether optimiser should be run and gets scalers
# try:
#     if reset:
#         raise Exception()
#     print("--- Get scaler's from file ---")
#     with open("src/data-small/scaler_store.txt") as f2:
#         scaler = eval(f2.readline())
#     if len(scaler) != len(masks):
#         raise Exception()
# except:
#     print("--- Get scaler's from optimisation ---")
#     scaler = run_minimize(masks, mask_neg=mask_sea, precision=1e-4) #mask_neg=mask_sea
#     print("--- Finished optimisation ---")
#     print("--- Optimiser Output ---")
#     print(scaler)
