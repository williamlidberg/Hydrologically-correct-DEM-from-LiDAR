from osgeo import gdal
from osgeo import ogr


def clip_raster(input_raster, input_shape, output_raster, nodata):
    OutTile = gdal.Warp(output_raster, 
                    input_raster, 
                    cutlineDSName=input_shape,
                    cropToCutline=True,
                    dstNodata = nodata)

    OutTile = None