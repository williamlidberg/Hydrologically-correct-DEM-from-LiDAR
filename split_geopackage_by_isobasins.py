import os
import argparse
import geopandas as gpd
from pathlib import Path
import pandas as pd

def main(isobasindir, geopackagedir, clipped_shapefiledir):
    # read all geopackages and concatinate them into a single dataframe
    # the big dataframe will be clipped by isobasins
    filepath = Path(geopackagedir)
    listoffiles = filepath.glob('*.gpkg')
    dataframes = []
    for geopackage in listoffiles:
        data = gpd.read_file(geopackage)
        dataframes.append(data)
    gdf = gpd.GeoDataFrame( pd.concat( dataframes, ignore_index=True), crs=dataframes[0].crs )
    # Drop colums that ESRI shape cant handle.
    gdf.drop(gdf.columns[5:22], axis=1, inplace=True)

    # print('clipping with isobasins')
    emptywatersheds = []
    for isobasin in os.listdir(isobasindir):
        if isobasin.endswith('.shp'):
            inputisobasin = gpd.read_file(isobasindir + isobasin)                      
            clippedout = clipped_shapefiledir + isobasin
            clipped = gpd.clip(gdf, inputisobasin)
            if clipped.empty:
                emptywatersheds.append(isobasin)
                continue
            # How wide are roads?
            #clipped['geometry'] = clipped.buffer(20)

            # How tall are roadbanks?
            #clipped['burndepth'] = 2
            clipped.to_file(clippedout, driver = 'ESRI Shapefile', encoding = 'utf-8')
    print('The following watersheds did not have any culverts', emptywatersheds)
 

if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('isobasindir', help='path to isobasin directory')   
    parser.add_argument('geopackagedir', help='path to dir with geopackages')     
    parser.add_argument('clipped_shapefiledir', help='path to directory with clipped culverts')
    args = vars(parser.parse_args())
    main(**args)