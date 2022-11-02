import argparse

from osgeo import gdal
from osgeo import ogr


def clip_raster(input_raster, input_shape, output_raster, nodata):
    OutTile = gdal.Warp(output_raster, 
                    input_raster, 
                    cutlineDSName=input_shape,
                    cropToCutline=True,
                    dstNodata = nodata)

    OutTile = None

# python3 
def main(vrt, polygon, clipeddem, nodata): 


    print('clip raster to isobasin outlines')
    clip_raster(vrt, polygon, clipeddem, nodata)

if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('vrt', help='path to ramdisk')   
    parser.add_argument('polygon', help='path to directory of all tiles')     
    parser.add_argument('clipeddem', help='path and name of output vrt')
    parser.add_argument('nodata', help='nodatavalue of the input raster',type=int)
    args = vars(parser.parse_args())
    main(**args)    