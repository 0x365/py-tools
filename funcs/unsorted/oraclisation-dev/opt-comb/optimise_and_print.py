from osgeo import gdal
from scipy.optimize import minimize
from func.func_matrix_to_image import *
from func.func_rms_optimiser import run_minimize
from func.func_maps import *
from PIL import Image

# Input image files
file_per_flood = r"/home/robert/oraclisation-dev/data/data-used/test_image.tif"
file_gov = r"/home/robert/oraclisation-dev/data/data-used/gov_working_test_image.tif"
file_google = r"/home/robert/oraclisation-dev/data/data-used/dartmout_observatory_output.tif"
file_global = r"/home/robert/oraclisation-dev/data/data-used/global_fl_database_flat.tif"
file_season = r"/home/robert/oraclisation-dev/data/data-used/seasonality_surface_water.tif" # Considered negative

out_file_confidence = r"/home/robert/oraclisation-dev/data/data-out/output_confidence.tif"
out_file_ins = r"/home/robert/oraclisation-dev/data/data-out/input_images.tif"
out_file_data = r"/home/robert/oraclisation-dev/data/data-out/output_with_rivers.tif"

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
del src_goo

 # Create strange mask manually
src_sea = gdal.Open(file_season)
mask_sea, max_sea = get_mask(src_sea, [0, 0, 4000, 4000])
mask_sea[mask_sea <= 1] = 0
mask_sea[mask_sea > 1] = 1
mask_sea[mask_sea == None] = 0
del src_sea

no = mask_gov.shape[0]*mask_gov.shape[1]




reset = 0    # Whether or not to generate new data or pull from file

# mask_names = ["mask_gov", "mask_glo", "mask_goo"]
# masks = [mask_gov, mask_glo, mask_goo]

# mask_names = ["mask_gov", "mask_glo", "mask_goo", "mask_per"]
# masks = [mask_gov, mask_glo, mask_goo, mask_per]

mask_names = ["Government Data", "Global Flood Database Data", "Dartmouth Observatory Data", "Permenant Water Database Data"]
masks = [mask_gov, mask_glo, mask_goo, mask_per]

# Remove permenant water
for i in range(len(masks)):
    masks[i] = masks[i]/np.amax(masks[i])
    masks[i] = masks[i] - mask_sea
    masks[i][masks[i] < 0] = 0


# Decide whether optimiser should be run and gets scalers
try:
    if reset:
        raise Exception()
    print("--- Get scaler's from file ---")
    with open("src/data-small/scaler_store.txt") as f2:
        scaler = eval(f2.readline())
    if len(scaler) != len(masks):
        raise Exception()
except:
    print("--- Get scaler's from optimisation ---")
    scaler = run_minimize(masks, precision=1e-4) #mask_neg=mask_sea
    print("--- Finished optimisation ---")
    print("--- Optimiser Output ---")
    print(scaler)
    

# Output final image with scalers applied
print("--- Convert Masks to Output Image ---")
matrix_to_image_func(masks, scaler, out_file_confidence, matrix_neg=mask_sea)
matrix_to_image_func(masks, scaler, out_file_data)
print("--- Finished ---")

for i in range(len(masks)):
    print(mask_names[i]+" - "+str(np.sum(masks[i]))+" - "+str(scaler[i])+" - "+str(np.sum(masks[i])*scaler[i]))

print("Masks Avg: "+str(np.sum(masks)/4))