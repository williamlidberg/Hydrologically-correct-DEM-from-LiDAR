import os
import geopandas as gpd
import pandas as pd
from geopandas.tools import sjoin
import glob
import shutil

# read lidar tile index to geopnadas dataframe
lidar_tiles_index = gpd.read_file('E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp')
path_to_block_metadata = 'E:/William/laserdataskog/20D001/metadata/'
json_list = []
for tile in os.listdir(path_to_block_metadata):
    if tile.endswith('.json'):
        name = path_to_block_metadata + tile
        tile_json = gpd.read_file(name)
        json_list.append(tile_json)
# merge all json polygons to a geopandas dataframe        
block_extent = gpd.GeoDataFrame(pd.concat(json_list, ignore_index=True), crs=json_list[0].crs)
# intersecct lidar tiles with block extent with one tile overlap
intersect = gpd.sjoin(lidar_tiles_index, block_extent, how='inner', op='intersects')
# get uniqe names
uniqe_names = intersect['LasNamn'].unique()


path_to_downloaded_data = 'E:/William/laserdataskog/pooled/'
path_to_working_dir = 'E:/William/laserdataskog/workdir/'
for tile in uniqe_names:
    downladed_tile = path_to_downloaded_data + tile + '.laz'
    copied_tile = path_to_working_dir + tile + '.laz'
    try:
        shutil.copy(downladed_tile, copied_tile)
    except:
        print('error',copied_tile)
