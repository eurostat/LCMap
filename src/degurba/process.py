from datetime import datetime
from rasterio.enums import Resampling
from pygridmap import gridtiler_raster
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.geotiff import replace_tiff_value, resample_geotiff_aligned

# tiling
# TODO deal with waters 310 ?


path = "/home/juju/geodata/gisco/degurba/"
years = [ "2021", "2011" ]
resolutions = [10000, 5000, 2000, 1000] #

#
os.makedirs("./tmp/degurba/", exist_ok=True)

# resampling
if True:
    for year in years:

        # prepare 1000m file with water set to no_data
        replace_tiff_value(path + "DGURBA_LEVEL2_GRD_"+year+"/DGUR_LEVEL2_GRD_1KM_"+year+"_extended.tif", "./tmp/degurba/"+year+"_1000.tif", 310, -9999)

        # aggregate other resolutions
        for resolution in resolutions:
            if resolution == 1000: continue
            print(datetime.now(), "resampling", year, resolution)
            resample_geotiff_aligned("./tmp/degurba/"+year+"_1000.tif", "./tmp/degurba/"+year+"_"+str(resolution)+".tif", resolution, resampling=Resampling.mode, dtype=np.int64)


if True:
    for resolution in resolutions:
        print(datetime.now(), "Tiling", resolution)

        # make folder for resolution
        folder_ = "./tmp/degurba/"+str(resolution)+"/"
        if not os.path.exists(folder_): os.makedirs(folder_)

        # prepare dict for geotiff bands
        dict = {}
        for year in years:
            dict["du" + year] = { "file" : "./tmp/degurba/"+year+"_"+str(resolution)+".tif", "band":1 }
        dict["T_2011"] = { "file" : "/home/juju/geodata/census/pop_20XX_"+str(resolution)+"m.tif", "band":2 }
        dict["T_2021"] = { "file" : "/home/juju/geodata/census/pop_20XX_"+str(resolution)+"m.tif", "band":4 }

        # launch tiling
        gridtiler_raster.tiling_raster(
            dict,
            folder_,
            crs="EPSG:3035",
            tile_size_cell = 512,
            format="parquet",
            num_processors_to_use = 10,
            )

        '''
        gridtiler_raster.tiling_raster_generic(
            dict,
            folder_,
            resolution,
            #x_min=0, y_min=0, x_max=0, y_max=0,
            -2820000,-3070000, 10030000, 5420000,
            crs="EPSG:3035",
            tile_size_cell = 512,
            format="parquet",
            num_processors_to_use = 10,
            )
        '''
