import os
import argparse
import geopandas as gpd
import pandas as pd
import shutil
from geopandas.tools import sjoin
import sys
import time
start_time = time.time()
sys.path.insert(1, 'C:/WhiteboxTools') #
#from wbt.whitebox_tools import WhiteboxTools # module call to WhiteboxTools... for more information see https://jblindsay.github.io/wbt_book/python_scripting/using_whitebox_tools.html)
from whitebox_tools import WhiteboxTools
# read lidar tile index to geopnadas dataframe
wbt = WhiteboxTools()
parser = argparse.ArgumentParser(description = 'Converts laz tiles to DEM tiles without edge effects')

#Example on how to run
#python E:/William/laserdataskog/process_new_block.py E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp E:/William/laserdataskog/20D001/ E:/William/laserdataskog/pooled/ E:/William/laserdataskog/workdir/ E:/William/laserdataskog/dem_dir/

def copy_tiles(tile_index, block_dir, pooled_laz_dir, copy_laz_dir):
    lidar_tiles_index = gpd.read_file(tile_index)
    path_to_block_metadata = block_dir + 'metadata/'
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
    uniqe_names = intersect['Indexruta'].unique()
    path_to_downloaded_data = pooled_laz_dir
    path_to_working_dir = copy_laz_dir
    names_relevant_tiles = []
    for name in os.listdir(path_to_downloaded_data):
        if name.endswith('.laz') and os.path.basename(name[7:20]) in uniqe_names:
            downladed_tile = path_to_downloaded_data + name
            copied_tile = path_to_working_dir + name
            shutil.copy(downladed_tile, copied_tile)
        
def laz_to_dem(copy_laz_dir): 
    wbt.set_verbose_mode(True)
    wbt.set_working_dir(copy_laz_dir)
    wbt.lidar_tin_gridding(parameter="elevation", 
    returns="last", # A DEM or DTM is usually obtained from the "last" returns, a DSM uses "first" returns (or better, use the lidar_digital_surface_model tool)
    resolution=0.5, # This is the spatial resolution of the output raster in meters and should depend on application needs and point density.
    exclude_cls= "0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18", # Example of classified points to be excluded from analysis i.e. class 9 is water.
    minz=None,
    maxz=None,
    max_triangle_edge_length=1000.0
    )
    print("Completed TIN interpolation \n")

def copy_completed_dems(block_dir, copy_laz_dir, dem_dir):
    for tile in os.listdir(block_dir):
        if tile.endswith('.laz'):
            dem = copy_laz_dir + tile.replace('.laz', '.tif')
            copied_dem = dem_dir + tile.replace('.laz', '.tif')
            shutil.copy(dem, copied_dem)

def main(tile_index, block_dir, pooled_laz_dir, copy_laz_dir, dem_dir):
    copy_tiles(tile_index, block_dir, pooled_laz_dir, copy_laz_dir)
    laz_to_dem(copy_laz_dir)
    copy_completed_dems(block_dir, copy_laz_dir, dem_dir)
    print("--- %s seconds ---" % (time.time() - start_time))
    
if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tile_index', help='Path to tile index shapefile that contain a column with names of each indexruta')    
    parser.add_argument('block_dir', help='path to the directory of lidar block')  
    parser.add_argument('pooled_laz_dir', help='Path to directory where all laz tiles are stored')
    parser.add_argument('copy_laz_dir', help='Path to directory where laztiles that intersects, and surround the block, are stored')
    parser.add_argument('dem_dir', help = 'Path to directory where final DEM tiles will be located.')
    args = vars(parser.parse_args())
    main(**args)
