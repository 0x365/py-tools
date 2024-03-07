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

def get_z(avg, p1, p2, p3):
    return ((p1-avg)*(p2-avg)*(p3-avg))
    #return math.sqrt((pow(p1-avg,2) + pow(p2-avg,2) + pow(p3-avg,2)))

def get_r(m1, m2):
    no = 4000 * 4000
    m_product = m1*m2
    m1_mean = np.average(m1)
    m2_mean = np.average(m2)
    m1_sq = m1*m1
    m2_sq = m2*m2
    top = np.sum(m_product - (no*m1_mean*m2_mean))
    bot1 = math.sqrt(np.sum(m1_sq)-(no*m1_mean*m1_mean))
    bot2 = math.sqrt(np.sum(m2_sq)-(no*m2_mean*m2_mean))
    if bot1 == 0 or bot2 == 0:
        return None
    return top/(bot1*bot2)

def get_rms(avg, m2):
    no = 4000 * 4000
    take = np.square(m2-avg)
    return math.sqrt(np.sum(take)/no)
    

xsize = 4000
ysize = 4000

min_sqrt = 100
print("Start")
for i in range(0, 30, 1):
    print(i)
    z_avg_li = []
    weight_x_li = []
    for ii in range(60, (100-i), 1):

        weight_gov = i/100
        weight_glo = ii/100
        weight_goo = (100-(i+ii))/100

        
        mask_gov_t = (mask_gov - mask_per) * weight_gov
        mask_glo_t = (mask_glo - mask_per) * weight_glo
        mask_goo_t = (mask_goo - mask_per) * weight_goo

        mask_gov_t[mask_gov_t < 0] = 0
        mask_glo_t[mask_glo_t < 0] = 0
        mask_goo_t[mask_goo_t < 0] = 0



        mask_comb = (mask_gov_t+mask_goo_t+mask_glo_t)/3



        rms1 = get_rms(mask_comb, mask_gov_t)
        rms2 = get_rms(mask_comb, mask_glo_t)
        rms3 = get_rms(mask_comb, mask_goo_t)

        # # Scorer
        # z = 0
        # for x in range(xsize):
        #     for y in range(ysize):
        #         z += get_z(mask_comb[x][y], mask_gov_t[x][y], mask_goo_t[x][y], mask_glo_t[x][y])
        #         if z > 5000 * xsize * ysize:
        #             break
        # if z < 5000 * xsize * ysize:
        #     avg_z = z/((xsize*ysize)-1)
        #     print(avg_z)

        del mask_gov_t
        del mask_glo_t
        del mask_goo_t
        sqrt = math.sqrt(pow(rms1,2)+pow(rms2,2)+pow(rms3,2))
        if sqrt < 15:
            z_avg_li.append(sqrt)
            weight_x_li.append(weight_glo)

        if sqrt < min_sqrt:
            min_sqrt = sqrt
            i_store = weight_gov
            ii_store = weight_glo
            iii_store = weight_goo
   
    if len(z_avg_li) > 0:
        plt.plot(weight_x_li, z_avg_li, label=("Weight Gov "+str(weight_gov)))

plt.ylabel('RMS')
plt.xlabel('Weight Glo')
plt.savefig(graph_file)
legend = plt.legend()

def export_legend(legend, filename="legend.png", expand=[-5,-5,5,5]):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)

export_legend(legend)

# mask_comb = mask_gov+mask_per
# driver = add_band(driver, mask_comb)
# export_map(driver, out_file)

print("Min Std: ", min_sqrt)
print("i (Gov) value: ", i_store)
print("ii (Glo) value: ", ii_store)
print("iii (Goo) value: ", iii_store)


del driver
del mask_gov
del mask_per
del mask_goo