from datetime import datetime
from rasterio.enums import Resampling
from pygridmap import gridtiler_raster
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.geotiff import resample_geotiff_aligned



resolutions = [200] #[10000, 5000, 2000, 1000, 500] #, 200, 100]
years = ["2012", "2006", "2000", "1990"] #2018
resampling = False
tiling = True



# resampling
if resampling:
    inpath = "/home/juju/geodata/CLC/"
    input_files = {
        "2018": "u2018_clc2018_v2020_20u1_raster100m/DATA/U2018_CLC2018_V2020_20u1.tif",
        "2012": "u2018_clc2012_v2020_20u1_raster100m/DATA/U2018_CLC2012_V2020_20u1.tif",
        "2006": "u2012_clc2006_v2020_20u1_raster100m/DATA/U2012_CLC2006_V2020_20u1.tif",
        "2000": "u2006_clc2000_v2020_20u1_raster100m/DATA/U2006_CLC2000_V2020_20u1.tif",
        "1990": "u2000_clc1990_v2020_20u1_raster100m/DATA/U2000_CLC1990_V2020_20u1.tif",
    }
    for resolution in resolutions:
        for year in years:
            print(datetime.now(), "resampling", year, resolution)
            infile = input_files[year]
            outfile = "./tmp/"+year+"_"+str(resolution)+".tif"
            resample_geotiff_aligned(inpath + infile, outfile, resolution, resampling=Resampling.mode, dtype=np.int8)


if tiling:
    # tiling
    for resolution in resolutions:
        for year in years:
            print(datetime.now(), "Tiling", year, resolution)

            # make folder for resolution
            # TODO
            folder_ = "/home/juju/Bureau/aaa/"+year+"/"+str(resolution)+"/"
            #folder_ = "./out/v1/"+year+"/"+str(resolution)+"/"
            if not os.path.exists(folder_): os.makedirs(folder_)

            # prepare dict for geotiff bands
            dict = {}
            dict["code"] = { "file" : "./tmp/"+year+"_"+str(resolution)+".tif", "band":1 }

            # launch tiling
            gridtiler_raster.tiling_raster(
                dict,
                folder_,
                crs="EPSG:3035",
                tile_size_cell = 512,
                format="parquet",
                num_processors_to_use = 10,
                #modif_fun = lambda v: int(v),
                )
