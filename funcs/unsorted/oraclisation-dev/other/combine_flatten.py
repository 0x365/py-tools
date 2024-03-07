import sys
from osgeo import gdal, osr
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math
from os import listdir
from os.path import isfile, join


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


folder_to_flatten = r"/home/robert/oraclisation-dev/data/data-manipulated/global_fl_database/"
out_file = r"/home/robert/oraclisation-dev/data/data-manipulated/global_fl_database_flat.tif"


onlyfiles = [f for f in listdir(folder_to_flatten) if isfile(join(folder_to_flatten, f))]

print("Number of flattenable files found: ", len(onlyfiles))

starting = 1
for file in onlyfiles:
    src = gdal.Open(folder_to_flatten+file)
    mask, max = get_mask(src, [0, 0, 4000, 4000], 2)
    if starting:
        mask_comb = mask
        starting = 0
    else:
        mask_comb += mask
    del mask
    del src

driver = create_map(4000, 4000)
driver = add_band(driver, mask_comb)
export_map(driver, out_file)

del driver

