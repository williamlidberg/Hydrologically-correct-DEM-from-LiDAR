import os
import argparse
import geopandas as gpd
from pathlib import Path
from tqdm import tqdm

def main(isobasindir, shapefile, clipped_shapefiledir):
    # only read large shapefile once to save time
    print('reading original shapefile')
    org_shapefile = gpd.read_file(shapefile)
    print('clipping with isobasins')
    #for isobasin in tqdm(os.listdir(isobasindir)):
    for isobasin in os.listdir(isobasindir):
        if isobasin.endswith('.shp'):
            inputisobasin = isobasindir + isobasin
            clip_shapefile = gpd.read_file(inputisobasin)        
            clippedout = clipped_shapefiledir + isobasin
            clipped = gpd.clip(org_shapefile, clip_shapefile)
            if not clipped.empty:            
                clipped.to_file(clippedout)
            else:
                print(isobasin, 'is empty')
                 

if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('isobasindir', help='path to isobasin directory')   
    parser.add_argument('shapefile', help='path to shapefile to be clipped')     
    parser.add_argument('clipped_shapefiledir', help='path to clipped shapefil directory')
    args = vars(parser.parse_args())
    main(**args)