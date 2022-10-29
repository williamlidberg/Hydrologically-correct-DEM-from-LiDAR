import os
import glob
import whitebox
import argparse
import shutil
import geopandas as gpd
from osgeo import ogr
from tqdm import tqdm

wbt = whitebox.WhiteboxTools()

def split_polygon(input_shape, split_shape_output):
    fn = input_shape 
    driver = ogr.GetDriverByName('ESRI Shapefile')  # See OGR Vector Format for other options
    dataSource = driver.Open(fn)
    layer = dataSource.GetLayer()
    sr = layer.GetSpatialRef()  # Spatial Reference
    dst = split_shape_output
    new_feat = ogr.Feature(layer.GetLayerDefn())  # Dummy feature

    for id, feat in enumerate(layer):
        new_ds = driver.CreateDataSource(r"{}\watershed_{}.shp".format(dst, id))
        new_lyr = new_ds.CreateLayer('watershed_{}'.format(id), sr, ogr.wkbPolygon) 
        geom = feat.geometry().Clone()
        new_feat.SetGeometry(geom)
        
        new_lyr.CreateFeature(new_feat)
        del new_ds, new_lyr

def buffer_basins(input_basin, buffered_basin):
    gdf = gpd.read_file(input_basin)
    gdf['geometry'] = gdf.geometry.buffer(0)
    gdf.to_file(buffered_basin)

def main(tempdir, dem, coastline, size, isobasins, split_isobasins):
    wbt.breach_depressions(
        dem, 
        output = tempdir + 'breached.tif', 
        max_depth=None, 
        max_length=None, 
        flat_increment=0.001, 
        fill_pits=True
    )

    wbt.isobasins(
        dem = tempdir + 'breached.tif', 
        output = tempdir + 'isobasins.tif', 
        size = size, 
        connections=True
    )

    wbt.raster_to_vector_polygons(
        i = tempdir + 'isobasins.tif', 
        output = tempdir + 'isobasins.shp'
    )

    wbt.erase(
        i = tempdir + 'isobasins.shp', 
        erase = coastline, 
        output = tempdir + 'erasedisobasins.shp'
    )
    # Isobasins are generated along the coast as well which
    # means that alot of small areas are created. Therefore polygons smaller than
    # 10 km2 were removed.
    gdf = gpd.read_file(tempdir + 'erasedisobasins.shp')
    gdf['geometry'].to_crs({'init': 'epsg:3006'})
    gdf['poly_area'] = gdf['geometry'].area/ 10**6
    gdf = gdf.loc[gdf['poly_area'] > 5]
    gdf.to_file(isobasins)
    
    print('explode isobasin shapefile')
    split_polygon(isobasins, tempdir)

    print('buffer isobasins')
    pathtoshapefiles = tempdir + '/*.shp'
    listofshapefiles = glob.glob(pathtoshapefiles)
    for basin in tqdm(listofshapefiles):
        bufferedbasin = split_isobasins + os.path.basename(basin)
        buffer_basins(basin, bufferedbasin)

    # clean up temp dir
    infile = tempdir + 'isobasins.csv'
    outfile = os.path.dirname(isobasins) + '/isobasins.csv'
    #shutil.copyfile(infile, outfile)
    for i in os.listdir(tempdir):
        os.remove(tempdir + i)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tempdir', help='path to ramdisk')     
    parser.add_argument('dem', help='path to the directory of 50 m dem')
    parser.add_argument('coastline', help='path to a shapefile of the coastline')
    parser.add_argument('size', help='target size of isobasins in int values', type=int)
    parser.add_argument('isobasins', help='path to output isobasin shapefile')
    parser.add_argument('split_isobasins', help='path to output isobasin dir for split isobasins')   
    args = vars(parser.parse_args())
    main(**args)