from osgeo import gdal
import numpy as np

def get_source_easy(file, dimensions):
    src = gdal.Open(file)
    mask, max = get_mask(src, [0, 0, 4000, 4000])
    mask[mask == None] = 0
    mask[mask < 0] = 0
    mask = mask/np.amax(mask)
    return mask

def create_map(xsize, ysize):
    driver = gdal.GetDriverByName('MEM').Create('', xsize, ysize, 0)
    return driver

def add_band(driver, mask):
    driver.AddBand()
    driver.GetRasterBand(driver.RasterCount).WriteArray(mask)
    return driver

def export_map(driver,location):
    output = gdal.GetDriverByName('GTiff').CreateCopy(location, driver)
    del output
    return

def get_mask(src_ds, c=[0,0,4000,4000], layer=1):
    band = src_ds.GetRasterBand(layer)
    if band.GetMinimum() is None or band.GetMaximum()is None:
        band.ComputeStatistics(0)
    return band.ReadAsArray(c[0], c[1], c[2], c[3]), band.GetMaximum()