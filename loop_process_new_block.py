import os
import argparse
import geopandas as gpd
import pandas as pd
import shutil
from geopandas.tools import sjoin
import sys
import time
import re
#import whitebox
#wbt = whitebox.WhiteboxTools()
sys.path.insert(1, 'E:/William/WBT') #
#from wbt.whitebox_tools import WhiteboxTools # module call to WhiteboxTools... for more information see https://jblindsay.github.io/wbt_book/python_scripting/using_whitebox_tools.html)
from whitebox_tools import WhiteboxTools
wbt = WhiteboxTools()
parser = argparse.ArgumentParser(description = 'Converts laz tiles to DEM tiles without edge effects')

start_time = time.time()
sys.path.insert(1, 'C:/WhiteboxTools') 

#Example on how to run
#python E:/William/laserdataskog/loop_process_new_block.py E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp E:/LAZ/original/ E:/William/laserdataskog/pooled/ E:/William/laserdataskog/workdir/ E:/William/laserdataskog/dem_dir/



def copy_tiles(tile_index, block_dir, pooled_laz_dir, copy_laz_dir):
    """
    looks trough the metadata directory for json files and their extent.
    The extent of all json files are then intersected with the lidar tile index to extract names
    of lidar tiles. Lidar tiles that intersect and soround the json extents are copied to a new directory.
    """
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
    print(len(uniqe_names), 'tiles intersected the block')
    path_to_downloaded_data = pooled_laz_dir
    path_to_working_dir = copy_laz_dir
    names_relevant_tiles = []
    for name in os.listdir(path_to_downloaded_data):
        if name.endswith('.laz') and os.path.basename(name[7:20]) in uniqe_names:
            downladed_tile = path_to_downloaded_data + name
            copied_tile = path_to_working_dir + name
            shutil.copy(downladed_tile, copied_tile)


def laz_to_dem(copy_laz_dir):
    """
    converts all laz tiles in a directory to a digital elevation raster.
    """ 
    wbt.set_verbose_mode(True)
    wbt.set_working_dir(copy_laz_dir)
    wbt.lidar_tin_gridding(parameter="elevation", 
    returns="last", # A DEM or DTM is usually obtained from the "last" returns, a DSM uses "first" returns (or better, use the lidar_digital_surface_model tool)
    resolution=0.5, # This is the spatial resolution of the output raster in meters and should depend on application needs and point density.
    exclude_cls= "0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18", # Example of classified points to be excluded from analysis i.e. class 9 is water.
    minz=None,
    maxz=None,
    max_triangle_edge_length=50
    )
    print("Completed TIN interpolation \n")



def move_completed_dems(block_dir, copy_laz_dir, dem_dir):
    """
    Parse names of the original tiles that make up a block and copies them to a new location.
    The boarder tiles used to create the DEM tiles are not copied.
    """
    for tile in os.listdir(block_dir):
        if tile.endswith('.laz'):
            dem = copy_laz_dir + tile.replace('.laz', '.tif')
            copied_dem = dem_dir + tile.replace('.laz', '.tif')
            try:
                shutil.move(dem, copied_dem)
            except:
                print('failed to move', dem)

def clean_temp_laz(copy_laz_dir):
    for root, dir, fs in os.walk(copy_laz_dir):
        for f in fs:
            if f.endswith('.laz'):
                os.remove(os.path.join(root, f))


def main(tile_index, root_dir, pooled_laz_dir, copy_laz_dir, dem_dir):
    for root, subdirectories, files in os.walk(root_dir):
        for subdirectory in subdirectories:
            if  re.match(r'^[0-9]{2}[A-Z][0-9]{3}$', subdirectory):
                block_dir = os.path.join(root,subdirectory + '/')
                print('Processing block', block_dir)
                copy_tiles(tile_index, block_dir, pooled_laz_dir, copy_laz_dir)
                print('copied laz files to work dir')
                laz_to_dem(copy_laz_dir)
                print('converted laz files to dem files')
                move_completed_dems(block_dir, copy_laz_dir, dem_dir)
                print('moved finished dem files to dem directory')
                clean_temp_laz(copy_laz_dir)
                print('cleaned temp dir')
                print("--- %s seconds ---" % (time.time() - start_time))


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tile_index', help='Path to tile index shapefile that contain a column with names of each indexruta')    
    parser.add_argument('root_dir', help='path to the directory of all lidar blocks')  
    parser.add_argument('pooled_laz_dir', help='Path to directory where all laz tiles are stored')
    parser.add_argument('copy_laz_dir', help='Path to directory where laztiles that intersects, and surround the block, are stored')
    parser.add_argument('dem_dir', help = 'Path to directory where final DEM tiles will be located.')
    args = vars(parser.parse_args())
    main(**args)
