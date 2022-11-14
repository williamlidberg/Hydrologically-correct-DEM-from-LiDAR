import os
import argparse
import glob
import pandas as pd
import geopandas as gpd
from pathlib import Path
from utils import clip


def main(tempdir, isobasindir, ditchdir, splitditchdir):
    print('merge shapefiles into geodataframe')
    shapefilepath = Path(ditchdir)
    listofshapefiles = shapefilepath.glob('*.shp')
    gdf = pd.concat([gpd.read_file(shp)
        for shp in listofshapefiles
        ]).pipe(gpd.GeoDataFrame)
    gdf.to_file('/data/test.shp')
    # print('clip geodataframe by watershed')
    # for isobasin in os.listdir(isobasindir):
    #     if isobasin.endswith('.shp'):
    #         inputisobasin = isobasindir + isobasin
    #         splitditch = splitditchdir + isobasin
    #         clip.clip_geopandas(gdf, inputisobasin, splitditch)

        
if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tempdir', help='path to temp directory') 
    parser.add_argument('isobasindir', help='path to isobasin directory')   
    parser.add_argument('ditchdir', help='path to dir with geopackages')     
    parser.add_argument('splitditchdir', help='path to directory with clipped culverts')
    args = vars(parser.parse_args())
    main(**args)