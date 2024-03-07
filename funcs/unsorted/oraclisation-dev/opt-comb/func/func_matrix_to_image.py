import numpy as np
from func.func_maps import *
from osgeo import osr


def matrix_to_image_func(matrix, scaler, out_file, matrix_neg=[0], none_img=False):

    xsize = matrix[0].shape[0]
    ysize = matrix[0].shape[1]
    # Create new map
    driver = create_map(xsize, ysize)

    for i in range(len(matrix)):
        matrix[i][matrix[i] == None] = 0
        max_val = np.amax(matrix[i])
        if max_val != 0:
            matrix[i] = matrix[i] * 255.0/max_val
        if len(matrix_neg) != len(matrix[i]):
            mask_i = matrix[i] * scaler[i]
        else:
            mask_i = (matrix[i]-(matrix_neg))
            mask_i = mask_i * scaler[i]
        mask_i[mask_i <= 0] = 0
        try:
            mask_comb += mask_i
        except:
            mask_comb = mask_i

    max_val = np.amax(mask_comb)
    mask_comb = mask_comb * 255.0/max_val
    mask_comb[mask_comb <= 6] = 0
    if none_img:
        mask_comb[mask_comb <= 0] = None
    
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    ulx = -3
    uly = 52
    xres = 1/4000
    yres = -1/4000
    xrot = 0
    yrot = 0
    geotransform = (ulx, xres, xrot, uly, yrot, yres)

    driver.SetGeoTransform(geotransform)
    driver.SetProjection(srs.ExportToWkt())

    driver = add_band(driver, mask_comb)
    driver.GetRasterBand(1).SetNoDataValue(0)
    export_map(driver, out_file)