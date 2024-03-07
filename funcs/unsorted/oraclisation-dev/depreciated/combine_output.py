import sys
from osgeo import gdal, osr
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math


def create_map(xsize, ysize):
    driver = gdal.GetDriverByName('MEM').Create('', xsize, ysize, 0)
    return driver

def add_band(driver, mask):
    driver.AddBand()
    driver.GetRasterBand(driver.RasterCount).WriteArray(mask)
    print("RasterCount: ", driver.RasterCount)
    return driver

def export_map(driver,location):
    output = gdal.GetDriverByName('GTiff').CreateCopy(location, driver)
    del output
    return

def get_mask(src_ds, c=[0,0,4000,4000], layer=1):
    band = src_ds.GetRasterBand(layer)
    if band.GetMinimum() is None or band.GetMaximum()is None:
        band.ComputeStatistics(0)
    print("----------")
    print("New Mask Created")
    print(band.GetNoDataValue())
    print(band.GetMinimum())
    print(band.GetMaximum())
    print("----------")
    return band.ReadAsArray(c[0], c[1], c[2], c[3]), band.GetMaximum()

def my_std(point1, point2, point3):
    avg = (point1 + point2 + point3)/3
    return math.sqrt( ( pow(point1-avg, 2) + pow(point2-avg, 2) + pow(point3-avg, 2) )/3)


file_per_flood = r"/home/robert/oraclisation-dev/data/data-manipulated/test_image.tif"
file_gov = r"/home/robert/oraclisation-dev/data/data-manipulated/gov_working_test_image.tif"
file_google = r"/home/robert/oraclisation-dev/data/data-manipulated/dartmout_observatory_output.tif"
file_global = r"/home/robert/oraclisation-dev/data/data-manipulated/global_fl_database_flat.tif"

test_file = r"/home/robert/oraclisation-dev/data/data-manipulated/dartmout_observatory_output_test.csv"

out_file = r"/home/robert/oraclisation-dev/data/data-manipulated/output.tif"
out_file2 = r"/home/robert/oraclisation-dev/data/data-manipulated/output2.tif"

graph_file = r"/home/robert/oraclisation-dev/data/data-manipulated/std_graph.png"

xsize = 4000
ysize = 4000

# Create new map
driver = create_map(xsize, ysize)

# Create Mask from Gov File
src_gov = gdal.Open(file_gov)
mask_gov, max_gov = get_mask(src_gov, [0, 0, xsize, ysize])
mask_gov[mask_gov == None] = 0
mask_gov = mask_gov * 255.0/max_gov
del src_gov

 # Create Mask from Input File
src_per_flood = gdal.Open(file_per_flood)
mask_per, max_per = get_mask(src_per_flood, [0, 0, xsize, ysize])
mask_per[mask_per == None] = 0
mask_per = mask_per * 255.0/max_per
del src_per_flood

 # Create Mask from Input File
src_goo = gdal.Open(file_google)
mask_goo, max_goo = get_mask(src_goo, [0, 0, xsize, ysize])
#mask_goo2[mask_goo2 == None] = 0
mask_goo[mask_goo == 0] = 10
mask_goo[mask_goo == 166] = 10
mask_goo[mask_goo == 208] = 10
mask_goo[mask_goo != 10] = 0
#mask_goo[mask_goo != 166 and mask_goo != ] = 0
mask_goo = mask_goo * 255.0/10
del src_goo

 # Create Mask from Input File
src_global = gdal.Open(file_global)
mask_glo, max_glo = get_mask(src_global, [0, 0, xsize, ysize])
mask_glo[mask_glo == None] = 0
mask_glo = mask_glo * 255.0/max_glo
del src_global

weight_gov = 0.1266
weight_goo = 0.8281
weight_glo = 0.0453

mask_gov_t = (mask_gov - mask_per) * weight_gov
mask_glo_t = (mask_glo - mask_per) * weight_glo
mask_goo_t = (mask_goo - mask_per) * weight_goo

mask_gov_t[mask_gov_t < 0] = 0
mask_glo_t[mask_glo_t < 0] = 0
mask_goo_t[mask_goo_t < 0] = 0



mask_comb = (mask_gov_t+mask_goo_t+mask_glo_t)
maxi = np.amax(mask_comb)
mask_comb = mask_comb * 255.0/maxi

driver = add_band(driver, mask_comb)
export_map(driver, out_file)

del mask_gov_t
del mask_goo_t
del mask_glo_t

del driver
del mask_gov
del mask_per
del mask_goo
del mask_glo