# Hydrologicall-correct-DEM-1m
This will be based on a combination of the old national lidar scan and the new national lidarscan (laserdata skog).

Since the entire 1 m DEM is to large to fit in memory it first need to be split into smaller parts. This was done by creating isobasins from a dem resampled to a resolution of 50m. These isobasins does not reach all the way to the coast so SMHIs subbasins were used for coastal areas.

# Data
1 m dem were created by the Swedish land use and cadastral registration authority and downloaded by SLU.\
Road culverts were downloaded from the Swedish traffic authority.\
Stream and road networks were extracted from the swedish property map.

# Set up docker
    docker build -t dem .
**Start container**

    docker run -it  --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest

## Create isobasins
40 000 grid cells equals to 100 km<sup>2</sup>

    python3 code/isobasins.py /temp/ /data/dem50m/dem_50m.tif /data/smhi/havsomraden2008_swe.shp 40000 /data/isobasins/isobasins.shp

## Unzip culverts
    python3 /code/utils/unzipfiles.py /data/culverts/







# Hydrologically-correct-DEM-from-LiDAR 05m - remove later
How to make a hydrollogically compatible DEM from a national LiDAR scan
The raw LiDAR data was downloaded from the Swedish mapping, cadastral and land registration authority (Lantmäteriet): https://www.lantmateriet.se/en/maps-and-geographic-information/geodataprodukter/produktlista/laserdata-nedladdning-skog/


# With docker container:
docker build -t dem .

**Start container**

docker run -it  --mount type=bind,source=/mnt/Extension_100TB/national_datasets/laserdataskog/,target=/data --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code dem:latest

**Create LiDAR Tile Footprint**\
python3 /code/lidar_tile_footprint.py 


**Select and copy relevant laztiles to new directory**
python3 /code/pool_laz_files.py 

once all data is pooled the script loop_process_new_block.py can be used to create DEM tiles without edgeeffects. This script uses the json files in the metadata directory of each block and intersect the block extent with a lidar tile index file. All laz files that intersect that extent gets copied to a new directory. This includes neighbouring tiles. DEM raster tiles are then created from the copied laz tiles but only tiles that are inside the block gets copied to the final output directory. This enables looping over lidar blocks and creating a seamless dem.  


# Process all existing blocks SFA
python E:/William/laserdataskog/loop_process_new_block.py E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp E:/LAZ/original/ E:/William/laserdataskog/pooled/ E:/William/laserdataskog/workdir/ E:/William/laserdataskog/dem_dir/



# Process all existing blocks docker - SLU
python3 /code/loop_process_new_block.py /code/data/Indexrutor_2_5km_Sverige.shp /data/original/ /data/pooled_laz_files/ /data/workdir/ /data/dem05m/

# Process all existing blocks docker - SLU test
python3 /code/loop_process_new_block.py /code/data/Indexrutor_2_5km_Sverige.shp /data/originaltest/ /data/pooled_laz_files/ /data/workdir/ /data/dem05m/


# Process all existing blocks SLU anaconda
python Y:/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/loop_process_new_block.py Y:/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/data/Indexrutor_2_5km_Sverige.shp Y:/national_datasets/laserdataskog/originaltest/ Y:/national_datasets/laserdataskog/pooled_laz_files/ G:/workdir/ Y:/national_datasets/laserdataskog/dem05m/

test

python Y:/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/loop_process_new_block.py Y:/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/data/Indexrutor_2_5km_Sverige.shp Y:/national_datasets/laserdataskog/originaltest/ Y:/national_datasets/laserdataskog/pooled_laz_files/ G:/workdir/ Y:/national_datasets/laserdataskog/dem05m/



# process new block
python E:/William/laserdataskog/loop_process_new_block.py E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp E:/William/newblock/20C045/ E:/William/laserdataskog/pooled/ E:/William/laserdataskog/workdir/ E:/William/laserdataskog/dem_dir/


python E:/William/laserdataskog/process_new_block.py E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp E:/William/newblock/20C045/ E:/William/laserdataskog/pooled/ E:/William/laserdataskog/workdir/ E:/William/newblockoutput/

# process remaining files from 2018, 2021 and new files from 2022
# new blocks are stored in E:/LAZ/2018/2022/ the script will loop over each block in this directory
python E:/William/laserdataskog/loop_process_new_block.py E:/William/Indexrutor/Indexrutor_2_5km_Sverige.shp E:/William/newblock/20C045/ E:/William/laserdataskog/pooled/ E:/William/laserdataskog/workdir/ E:/William/laserdataskog/dem_dir/


