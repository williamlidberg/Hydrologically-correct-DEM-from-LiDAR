# Hydrologicall-correct-DEM-1m
This will be based on a combination of the old national lidar scan and the new national lidarscan (laserdata skog).

Since the entire 1 m DEM is to large to fit in memory it first need to be split into smaller parts. This was done by creating isobasins from a dem resampled to a resolution of 50m. These isobasins does not reach all the way to the coast so SMHIs subbasins were used for coastal areas.

# Data
1 m dem were created by the Swedish land use and cadastral registration authority and downloaded by SLU.\
Road culverts were downloaded from the Swedish traffic authority.\
Stream and road networks were extracted from the swedish property map.

# Set up docker
Navigate to the dockerfile and build container.
cd /mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/

    docker build -t dem .
**Start container**

    docker run -it  --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest


b5ff4579177:

# Prepare data

# memory testing

    **breaching worked for 800km2 and used 45 GB RAM**
    **Breach for 160000km2 used 77 GB RAM. it took 360 min***
    **DTW 60GB 1h11 min** 
    **DTW 106GB 2h12 m** 
    **Clipp**
   


## Create isobasins

Isobasins between 2 Isobasins between 2 kmkm<sup>2</sup> and 2030 kmkm<sup>2</sup>
 and 2030 Isobasins between 2 kmkm<sup>2</sup> and 2030 kmkm<sup>2</sup>


python3 code/create_isobasins.py /temp/ /data/dem50m/dem_50m.tif /data/smhi/havsomraden2008_swe.shp 640000 /data/isobasins/isobasins.shp /data/isobasins/split/

1313 watersheds were produced

# Clip input data with isobasins

## Clip rasters

**Clip dem**

    python3 code/split_raster_by_isobasins.py temp/ /national/Swedish1mDEM_old/tiles/ /national/Swedish1mDEM_old/mosaic1m.vrt data/isobasins/split_isobasins/ data/clipraster/dem/ -32768

**Clip Ditches**

Fillburn failed on the tiles so a normal subtract will be used instead. Instead of burning the classified ditches I have decided to burn the probability instead. The probability was originaly between 0 and 100. I reclassified all probabilities under 50% to 0 and rescaled the values from 0-100 to 0-1. The reclassified raster were then subtracted from the original DEM with the pixel values. This meant that the min ditch burn depth is 0.5 m and the max burn depth is 1 m. 

    python3 code/reclassify_ditches.py /national/ditches/1m/probability/ /data/reclassified_ditches/

convert ditches to vrt and clip with isobasins

    python3 code/split_ditches_by_isobasins.py /temp/ /data/reclassified_ditches/ /data/ditches1m.vrt /data/isobasins/split/ /data/reclassified_ditches/ -32768



## Clip vectors

**Clip Roads and railroads**
Streams were burned across roads and railroads in order to let the water pass. A merged shapefile containing both roads and railroads were clipped by the outlines of the isobasins.

    python3 code/split_vector_by_isobasins.py /data/isobasins/split/ /data/fastighetskartan/2021-08-09/roads_railroads.shp /data/clipvector/roads_rail/

    
**Clip Streams**
Streams from the propertymap were also clipped to the outline of the isobasins.

    python3 code/split_vector_by_isobasins.py /data/isobasins/split/ /data/fastighetskartan/2021-08-09/delivery/topo/fastighk/riks/vl_riks.shp /data/clipvector/streams/

**Clip Culverts**
    python3 code/split_culvert_by_isobasins.py /data/isobasins/split/ /data/culverts/ /data/clipvector/culverts/

**Identify catchments without roads, streams, culverts or ditches**

# Preprocessing

The preprocessing is done to create a hydrologically compatible DEM and was done in x stepps. 
    1. AI detected ditch channels were burned into the DEM .
    2. streams were burned across roads and railroads for a maximum of 50 meters.
    3. Road

    python3 code/preprocess.py /temp/ /data/clipraster/ /data/clipditches/ /data/clipculverts/ /data/cliproads/ /data/cliprailroads/ /data/clipstreams/ /data/breachedwatersheds/
    # krycklan
    python3 code/preprocess.py /temp/ /data/krycklan/dem/ /data/clipditches/ /data/clipculverts/ /data/cliproads/ /data/cliprailroads/ /data/clipstreams/ /data/krycklan/breacheddem/

    # Topographical modeling for hydrological features

    python3 code/Flowaccumulation.py /data/breachedwatersheds/ /data/D8pointer/ /data/D8flowaccumulation/



**Unzip culverts**
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


