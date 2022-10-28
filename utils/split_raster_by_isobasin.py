import os
import glob
import argparse
from osgeo import gdal
from osgeo import ogr
import geopandas as gpd
from tqdm import tqdm


def split_polygon(input_shape, split_shape_output):
    fn = input_shape 
    driver = ogr.GetDriverByName('ESRI Shapefile')  # See OGR Vector Format for other options
    dataSource = driver.Open(fn)
    layer = dataSource.GetLayer()
    sr = layer.GetSpatialRef()  # Spatial Reference
    dst = split_shape_output
    new_feat = ogr.Feature(layer.GetLayerDefn())  # Dummy feature

    for id, feat in enumerate(layer):
        new_ds = driver.CreateDataSource(r"{}\feat_{}.shp".format(dst, id))
        new_lyr = new_ds.CreateLayer('feat_temp_{}'.format(id), sr, ogr.wkbPolygon) 
        geom = feat.geometry().Clone()
        new_feat.SetGeometry(geom)
        
        new_lyr.CreateFeature(new_feat)
        del new_ds, new_lyr

def buffer_basins(input_basin, buffered_basin):
    gdf = gpd.read_file(input_basin)
    gdf['geometry'] = gdf.geometry.buffer(0)
    gdf.to_file(buffered_basin)
    
def clip_raster(input_raster, input_shape, output_raster):
    OutTile = gdal.Warp(output_raster, 
                    input_raster, 
                    cutlineDSName=input_shape,
                    cropToCutline=True,
                    dstNodata = 0)

    OutTile = None

# example: python3 code/utils/split_raster_by_isobasin.py temp/ dem/tilessinglefolder/ dem/mosaic1m.vrt data/isobasins/ data/clipraster/
def main(tempdir, tilepath, vrtpath, isobasins, clipdir): 
    
    print('build vrt')
    old_val = gdal.GetConfigOption("GDAL_NUM_THREADS")
    gdal.SetConfigOption('GDAL_NUM_THREADS', '127')
    pathtotiles = tilepath + '/*.tif'  
    listoftiles = glob.glob(pathtotiles)
    vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic', addAlpha=False)
    gdal.BuildVRT(vrtpath, listoftiles, options=vrt_options)

    print('explode isobasin shapefile')
    split_polygon(isobasins, tempdir)

    print('buffer isobasins')
    pathtoshapefiles = tempdir + '/*.shp'
    listofshapefiles = glob.glob(pathtoshapefiles)
    for basin in tqdm(listofshapefiles):
        bufferedbasin = tempdir + os.path.basename(basin)
        buffer_basins(basin, bufferedbasin)

    print('clip raster to isobasin outlines')
    pathtoshapefiles = tempdir + '/*.shp'  
    listofshapefiles = glob.glob(pathtoshapefiles)
    for basin in tqdm(listofshapefiles):
        outname = clipdir + os.path.basename(basin).replace('.shp', '.tif')
        clip_raster(vrtpath, basin, outname)

    print('cleaning temp dir')
    for i in os.listdir(tempdir):
        os.remove(tempdir + i)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tempdir', help='path to ramdisk')   
    parser.add_argument('tilepath', help='path to directory of all tiles')     
    parser.add_argument('vrtpath', help='path and name of output vrt')
    parser.add_argument('isobasins', help='path and name of shapefile containing isobasins')     
    parser.add_argument('clipdir', help='path to the output directory for clipped isobains')

    args = vars(parser.parse_args())
    main(**args)