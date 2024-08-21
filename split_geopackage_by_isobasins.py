import os
import argparse
import geopandas as gpd
from pathlib import Path
import pandas as pd

# python3 /code/split_geopackage_by_isobasins.py /data/split/ /data/culvertsGeopackage/ /data/clipVector/culverts_line/

def main(isobasindir, geopackagedir, clipped_shapefiledir):
    # Read all geopackages and concatenate them into a single dataframe
    filepath = Path(geopackagedir)
    listoffiles = filepath.glob('*.gpkg')
    dataframes = []
    for geopackage in listoffiles:
        data = gpd.read_file(geopackage)
        dataframes.append(data)
    gdf = gpd.GeoDataFrame(pd.concat(dataframes, ignore_index=True), crs=dataframes[0].crs)
    
    # Drop columns that ESRI Shapefile can't handle
    gdf.drop(gdf.columns[5:22], axis=1, inplace=True)

    # Filter for LineString and MultiLineString geometries only
    gdf = gdf[gdf.geometry.type.isin(['LineString', 'MultiLineString'])]

    # Clip with isobasins
    emptywatersheds = []
    for isobasin in os.listdir(isobasindir):
        if isobasin.endswith('.shp'):
            inputisobasin = gpd.read_file(os.path.join(isobasindir, isobasin))
            clippedout = os.path.join(clipped_shapefiledir, isobasin)
            clipped = gpd.clip(gdf, inputisobasin)

            # Filter the clipped data for LineString and MultiLineString geometries again (just in case)
            clipped = clipped[clipped.geometry.type.isin(['LineString', 'MultiLineString'])]

            if clipped.empty:
                emptywatersheds.append(isobasin)
                print(isobasin, 'empty')
                continue

            clipped.to_file(clippedout, driver='ESRI Shapefile', encoding='utf-8')

    print('The following watersheds did not have any culverts:', emptywatersheds)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contain training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('isobasindir', help='path to isobasin directory')
    parser.add_argument('geopackagedir', help='path to dir with geopackages')
    parser.add_argument('clipped_shapefiledir', help='path to directory with clipped culverts')
    args = vars(parser.parse_args())
    main(**args)