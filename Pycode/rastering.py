#!/usr/bin/env python3
"""Nicolas Gampierakis (2019), rutgerhofste (2015).
Performs raster operations.
"""

import rasterio
import rasterio.plot
import pyproj
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import georaster
from osgeo import osr
import scipy.io
import numpy as np
from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr
import matplotlib.pylab as plt
import re
import os
import glob


def asc_convert(file_name):
    """
    Args:
        file_name (str): name of text file to be converted to ASCII raster.
        Can use search
    Returns:


    """
    txt_in = "./rasters/asc_loose/" + str(file_name) + ".txt"
    asc_out = "./rasters/asc_loose/" + str(file_name) + ".asc"
    f = open(txt_in, "r")
    filedata = f.read()
    f.close()
    newdata = re.sub("\s+", " ", filedata).strip()
    newdata = re.sub(",", " ", newdata).strip()
    newdata = re.sub(";", "\n", newdata).strip()
    # newdata = filedata.replace(r" +", r" ")
    print(newdata)
    f = open(asc_out, "w")
    f.write(newdata)
    f.close()


def asc_to_tif(q_num):
    """
    Converts ASCII raster file into tiff image format
    Args:
        q_num (str): filename of fclim raster. Can use search_for_files()
            to generate list of valid files.
    """
    drv = gdal.GetDriverByName("GTiff")
    in_path = "./rasters/asc_loose/q" + str(q_num) + ".asc"
    out_path = "./rasters/gen_tif/q" + str(q_num) + ".tif"
    ds_in = gdal.Open(in_path)
    ds_out = drv.CreateCopy(out_path, ds_in)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(31254)
    ds_out.SetProjection(srs.ExportToWkt())
    ds_in = None
    ds_out = None


def read_file(filename):
    """
    Authors:
        rutgerhofste (2015)

    Args:

    Returns:

    """
    filehandle = gdal.Open(filename)
    band1 = filehandle.GetRasterBand(1)
    geotransform = filehandle.GetGeoTransform()
    geoproj = filehandle.GetProjection()
    Z = band1.ReadAsArray()
    xsize = filehandle.RasterXSize
    ysize = filehandle.RasterYSize
    return xsize, ysize, geotransform, geoproj, Z


def write_file(filename, geotransform, geoprojection, data):
    """
    Authors:
        rutgerhofste (2015)

    Args:

    Returns:

    """
    (x, y) = data.shape
    file_format = "GTiff"
    driver = gdal.GetDriverByName(file_format)
    # you can change the data format but be sure to be able to store negative
    # values including -9999
    dst_datatype = gdal.GDT_Float64
    dst_ds = driver.Create(filename, y, x, 1, dst_datatype)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(geoprojection)
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
    dst_ds = None
    return 1


def search_for_files(search_criteria="q*.tif"):
    dirpath = r"./rasters"
    # search_criteria = "*_new.tif"
    q = os.path.join(dirpath, search_criteria)
    print(q)
    dem_fps = glob.glob(q)
    return dem_fps


def tiff_transform(q_num_list, weight_list):
    """
    Authors:
        rutgerhofste (2015), Nicolas Gampierakis (2019)

    Args:

    Returns:

    """
    firstrun = 1
    sum_weight = sum(weight_list)
    for q_num in q_num_list:
        in_path = "./rasters/gen_tif/q" + str(q_num) + ".tif"
        out_path = "./rasters/proc_tif/q" + str(q_num) + ".tif"
        index = q_num_list.index(q_num)
        weight = weight_list[index]
        if firstrun == 1:
            [xsize, ysize, geotransform, geoproj, Z] = read_file(in_path)

            Z = Z * weight / sum_weight

            Z[np.isnan(Z)] = -9999
            new_geotransform = (
                geotransform[0],
                geotransform[1],
                geotransform[2],
                geotransform[3],
                geotransform[4],
                -1 * geotransform[5],
            )
            print(new_geotransform)
            # set the new GeoTransform, effectively flipping the image
            write_file(out_path, new_geotransform, geoproj, Z)
