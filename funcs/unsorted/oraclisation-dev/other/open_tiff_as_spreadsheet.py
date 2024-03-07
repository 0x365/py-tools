import sys
from osgeo import gdal, osr
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math


file_in = r"/home/robert/oraclisation-dev/src/output.tif"
file_out = r"/home/robert/oraclisation-dev/data/data-out/spreadsheet_view.csv"

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

src = gdal.Open(file_in)
mask, max = get_mask(src, [0, 0, 4000, 4000])

np.savetxt(file_out, mask, delimiter=",")