import os
import geopandas as gpd
import pandas as pd
from geopandas.tools import sjoin
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
len(intersect['LasNamn'].unique())
