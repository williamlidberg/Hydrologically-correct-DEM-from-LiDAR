from osgeo import gdal
from osgeo import ogr
import geopandas as gpd

def clip_raster(input_raster, input_shape, output_raster, nodata):
    OutTile = gdal.Warp(output_raster, 
                    input_raster, 
                    cutlineDSName=input_shape,
                    cropToCutline=True,
                    dstNodata = nodata)
    OutTile = None

def clip_shapefile(input_shapefile, clip_input_shape, output_vector):
    org_shapefile = gpd.read_file(input_shapefile)
    clip_shapefile = gpd.read_file(clip_input_shape)
    clipped = gpd.clip(org_shapefile, clip_shapefile)
    clipped.to_file(output_vector)

def clip_geopackage(input_geopackage, clip_input_shape, output_vector):
    geopackage = gpd.read_file(input_geopackage, driver = 'shape')
    shape = gpd.read_file(clip_input_shape)
    clipped = gpd.clip(geopackage, shape)
    clipped.to_file(output_vector)

