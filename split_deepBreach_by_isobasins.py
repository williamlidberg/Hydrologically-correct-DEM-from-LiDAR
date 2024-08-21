import os
import argparse
import geopandas as gpd
from pathlib import Path
import pandas as pd
from shapely.validation import make_valid


#  python3 /code/split_deepBreach_by_isobasins.py /data/split/ /culverts/vector/ /data/clipvector/deepBreach
#  python3 /code/split_deepBreach_by_isobasins.py /data/split/ /data/tempculvert/ /data/clipvector/deepBreach

def main(isobasindir, culvertdir, clipped_shapefiledir):
    filepath = Path(culvertdir)
    listoffiles = filepath.glob('*.shp')
    dataframes = []
    for shapefile in listoffiles:
        data = gpd.read_file(shapefile)
        
        # Fix invalid geometries
        data['geometry'] = data['geometry'].apply(lambda geom: make_valid(geom))
        
        # Apply a tiny buffer to all geometries to ensure lines become polygons
        data['geometry'] = data['geometry'].buffer(0.01)
        
        # Filter out polygons with a perimeter larger than 100 meters
        data = data[data['geometry'].length <= 100]
        
        dataframes.append(data)

    gdf = gpd.GeoDataFrame(pd.concat(dataframes, ignore_index=True), crs=dataframes[0].crs)
    
    emptywatersheds = []
    for isobasin in os.listdir(isobasindir):
        if isobasin.endswith('.shp'):
            inputisobasin = gpd.read_file(os.path.join(isobasindir, isobasin))                      
            clippedout = os.path.join(clipped_shapefiledir, isobasin)
            
            clipped = gpd.clip(gdf, inputisobasin)
            
            if clipped.empty:
                emptywatersheds.append(isobasin)
                continue
            
            clipped.to_file(clippedout, driver='ESRI Shapefile', encoding='utf-8')
            print('clipped', isobasin)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('isobasindir', help='path to isobasin directory')   
    parser.add_argument('culvertdir', help='path to dir with shapefiles')     
    parser.add_argument('clipped_shapefiledir', help='path to directory with clipped shapefiles')
    args = vars(parser.parse_args())
    main(**args)