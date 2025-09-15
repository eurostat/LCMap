from datetime import datetime
from rasterio.enums import Resampling
from pygridmap import gridtiler_raster
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.geotiff import resample_geotiff_aligned

inpath = "/home/juju/geodata/CLC/"
resolutions = [10000, 5000, 2000, 1000, 500, 200, 100]


#/home/juju/geodata/CLC/u2000_clc1990_v2020_20u1_raster100m/DATA/U2000_CLC1990_V2020_20u1.tif


# resampling
for resolution in resolutions:
    for year in ["2018", "2012", "2006", "2000", "1990"]:
        print(datetime.now(), "resampling", year, resolution)
        infile = "u2000_clc"+year+"_v2020_20u1_raster100m/DATA/U2000_CLC"+year+"_V2020_20u1.tif"
        resample_geotiff_aligned(inpath + infile, "./tmp/"+year+"_"+str(resolution)+".tif", resolution, resampling=Resampling.mode, dtype=np.int8)


'''
# tiling
# TODO modify gridtiler to ignore value=10 (water)
for resolution in resolutions:
    print(datetime.now(), "Tiling", resolution)

    # make folder for resolution
    folder_ = path+"out/"+str(resolution)+"/"
    if not os.path.exists(folder_): os.makedirs(folder_)

    # prepare dict for geotiff bands
    dict = {}
    for year in ["2024"]: #TODO check that
        dict["du" + year] = {"file":path + "/out/"+str(resolution)+".tif", "band":1}

    # launch tiling
    gridtiler_raster.tiling_raster(
        dict,
        folder_,
        crs="EPSG:3035",
        tile_size_cell = 512,
        format="parquet",
        num_processors_to_use = 8,
        #modif_fun = lambda v: int(v),
        )
'''
