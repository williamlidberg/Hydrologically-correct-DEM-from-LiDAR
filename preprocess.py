import os
import whitebox
import argparse
import glob
import geopandas as gpd
from tqdm import tqdm
wbt = whitebox.WhiteboxTools()



def main(tempdir, demdir, culvertdir, ditchdir, roaddir, railroaddir, streamdir, breacheddir):
    for watershed in os.listdir(demdir):
        if watershed.endswith('.tif'):
            wbt.breach_depressions(
            dem = demdir + watershed, 
            output = breacheddir + watershed, 
            max_depth=None, 
            max_length=None, 
            flat_increment=None, 
            fill_pits=True
            )




if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tempdir', help='path to ramdisk')     
    parser.add_argument('demdir', help='path to the directory of 50 m dem')
    parser.add_argument('ditchdir', help='path to a shapefile of the coastline')
    parser.add_argument('culvertdir', help='path to a shapefile of the coastline')
    parser.add_argument('roaddir', help='target size of isobasins in int values')
    parser.add_argument('railroaddir', help='path to output isobasin shapefile')
    parser.add_argument('streamdir', help='path to output isobasin shapefile')  
    parser.add_argument('breacheddir', help='path to output isobasin shapefile') 
    args = vars(parser.parse_args())
    main(**args)