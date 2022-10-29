import os
import geopandas as gpd
import pandas as pd
import shutil
from geopandas.tools import sjoin
import sys
try:
    sys.path.insert(1, 'E:/William/WBT') #
    from whitebox_tools import WhiteboxTools
    wbt = WhiteboxTools()
except: 
    print('failed to import local whitebox, using pip instead')
else:
    import whitebox as wbt
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
uniqe_names = intersect['Indexruta'].unique()


path_to_downloaded_data = 'E:/William/laserdataskog/pooled/'
path_to_working_dir = 'E:/William/laserdataskog/workdir/'
names_relevant_tiles = []
for name in os.listdir(path_to_downloaded_data):
    if name.endswith('.laz') and os.path.basename(name[7:20]) in uniqe_names:
        downladed_tile = path_to_downloaded_data + name
        copied_tile = path_to_working_dir + name
        shutil.copy(downladed_tile, copied_tile)
        
        
# Function to gather the file names of TIF files and puts them in a list
def find_tif_files(input_directory): # finds TIF files in an input directory
    files = os.listdir(input_directory)
    file_names = []
    for f in files:
        if f.endswith(".tif"): #change accordingly for appropriate raster type 
            file_names.append(f)
    return file_names


def main():
    ########################
    # Set up WhiteboxTools #
    ########################
    wbt = WhiteboxTools()
    wbt.set_verbose_mode(False) # Sets verbose mode. If verbose mode is False, tools will not print output messages
    #wbt.set_compress_rasters(True) # Compressed TIF file format based on the DEFALTE algorithm
    in_directory = 'E:/William/laserdataskog/workdir/' # Input file directory; change to match your environment

    wbt.set_working_dir(in_directory)
    wbt.lidar_tin_gridding(parameter="elevation", 
    returns="last", # A DEM or DTM is usually obtained from the "last" returns, a DSM uses "first" returns (or better, use the lidar_digital_surface_model tool)
    resolution=0.5, # This is the spatial resolution of the output raster in meters and should depend on application needs and point density.
    exclude_cls= "0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18", # Example of classified points to be excluded from analysis i.e. class 9 is water.
    minz=None,
    maxz=None,
    max_triangle_edge_length=50.0
    )
    print("Completed TIN interpolation \n")

    
main()
