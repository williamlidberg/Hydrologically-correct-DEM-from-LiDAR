# Hydrologically-correct-DEM-from-LiDAR
How to make a hydrollogically compatible DEM ffrom a national LiDAR scan
The raw LiDAR data was downloaded from the Swedish mapping, cadastral and land registration authority (Lantmäteriet): https://www.lantmateriet.se/en/maps-and-geographic-information/geodataprodukter/produktlista/laserdata-nedladdning-skog/

Whitebox tools uses data from nearby tiles but in order for this to work all tiles need to be stored in the same directory. The raw data is stored in  multiple subdirectories as .laz files. Use the script pool_laz_files.py to copy all tiles in the same directory. 

once all data is pooled the script loop_process_new_block.py can be used to create DEM tiles without edgeeffects. This script uses the json files in the metadata directory of each block and intersect the block extent with a lidar tile index file. All laz files that intersect that extent gets copied to a new directory. This includes neighbouring tiles. DEM raster tiles are then created from the copied laz tiles but only tiles that are inside the block gets copied to the final output directory. This enables looping over lidar blocks and creating a seamless dem.  


## Select and copy relevant laztiles to new directory
python E:/William/laserdataskog/Select_lidar_tiles.py

# Process all existing blocks
python E:/William/laserdataskog/loop_process_new_block.py E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp E:/LAZ/original/ E:/William/laserdataskog/pooled/ E:/William/laserdataskog/workdir/ E:/William/laserdataskog/dem_dir/

# process 2018
python E:/William/laserdataskog/loop_process_new_block.py E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp E:/LAZ/2018/2018/ E:/William/laserdataskog/pooled/ E:/William/laserdataskog/workdir/ E:/William/laserdataskog/dem_dir/

# process remaining files from 2018, 2021 and new files from 2022
# new blocks are stored in E:/LAZ/2018/2022/ the script will loop over each block in this directory
python E:/William/laserdataskog/loop_process_new_block.py E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp E:/LAZ/2018/ E:/William/laserdataskog/pooled/ E:/William/laserdataskog/workdir/ E:/William/laserdataskog/dem_dir/
