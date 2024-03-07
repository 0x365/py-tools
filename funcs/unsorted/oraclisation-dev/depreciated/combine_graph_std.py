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

out_file = r"/home/robert/oraclisation-dev/data/data-manipulated/output.tif"
out_file2 = r"/home/robert/oraclisation-dev/data/data-manipulated/output2.tif"

graph_file = r"/home/robert/oraclisation-dev/data/data-manipulated/std_graph.png"

# Create new map
driver = create_map(4000, 4000)

# Create Mask from Gov File
src_gov = gdal.Open(file_gov)
mask_gov, max_gov = get_mask(src_gov, [0, 0, 4000, 4000])
mask_gov[mask_gov == None] = 0
mask_gov = mask_gov * 255.0/max_gov
del src_gov

 # Create Mask from Input File
src_per_flood = gdal.Open(file_per_flood)
mask_per, max_per = get_mask(src_per_flood, [0, 0, 4000, 4000])
mask_per[mask_per == None] = 0
mask_per = mask_per * 255.0/max_per
del src_per_flood

 # Create Mask from Input File
src_global = gdal.Open(file_global)
mask_glo, max_glo = get_mask(src_global, [0, 0, 4000, 4000])
mask_glo[mask_glo == None] = 0
mask_glo = mask_glo * 255.0/max_glo
del src_global

 # Create Mask from Input File
src_goo = gdal.Open(file_google)
mask_goo, max_goo = get_mask(src_goo, [0, 0, 4000, 4000])
#mask_goo2[mask_goo2 == None] = 0
mask_goo[mask_goo == 0] = 10
mask_goo[mask_goo == 166] = 10
mask_goo[mask_goo == 208] = 10
mask_goo[mask_goo != 10] = 0
#mask_goo[mask_goo != 166 and mask_goo != ] = 0
mask_goo = mask_goo * 255.0/10
del src_goo

std_min = 100
print("Start")
for i in range(0, 11, 1):
    std_avg_li = []
    weight_x_li = []
    for ii in range(0, (10-i+1), 1):

        weight_gov = i/10
        weight_glo = ii/10
        weight_goo = (10-(i+ii))/10

        
        mask_gov_t = (mask_gov * weight_gov) - mask_per
        mask_glo_t = (mask_glo * weight_glo) - mask_per
        mask_goo_t = (mask_goo * weight_goo) - mask_per

        mask_gov_t[mask_gov_t < 0] = 0
        mask_glo_t[mask_glo_t < 0] = 0
        mask_goo_t[mask_goo_t < 0] = 0



        mask_comb = (mask_gov_t+mask_goo_t+mask_glo_t)/3


        std_sum = 0
        for x in range(len(mask_gov)):
            for y in range(len(mask_gov)):
                std_sum += my_std(mask_gov_t[x][y], mask_glo_t[x][y], mask_goo_t[x][y])

        del mask_gov_t
        del mask_glo_t
        del mask_goo_t

        std_avg = std_sum/(len(mask_gov)*len(mask_gov))
        print("Loop: ", ii)
        print("Std of data: ", std_avg)

        if std_avg < 10:
            std_avg_li.append(std_avg)
            weight_x_li.append(weight_glo)
        
        if std_avg < std_min:
            std_min = std_avg
            i_store = i
            ii_store = ii
            
    if len(std_avg_li) > 0:
        plt.plot(weight_x_li, std_avg_li, marker="o", label=str(i))

plt.ylabel('Avg Std')
plt.xlabel('Weight Per (1 - Weight Gov)')
plt.legend()
plt.savefig(graph_file)

# mask_comb = mask_gov+mask_per
# driver = add_band(driver, mask_comb)
# export_map(driver, out_file)

print("Min Std: ", std_min)
print("i value: ", i_store)
print("ii value: ", ii_store)


del driver
del mask_gov
del mask_per
del mask_goo