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

    docker run -it  --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest

# Prepare data

# memory testing

    **breaching worked for 800km2 and used 45 GB RAM**
    **Breach for 160000km2 used 77 GB RAM. it took 360 min***
    **DTW 60GB 1h11 min** 
    **DTW 106GB 2h12 m** 
    **Clipp**
   
   python3 code/temp/memorytest.py national/Swedish1mDEM_old/mosaic1m.vrt /data/isobasins/3200km2/split/watershed_351.shp data/memorytest/dem/watershed_351.tif -32768
   
   python3 code/temp/memorytest.py national/Swedish1mDEM_old/mosaic1m.vrt /data/isobasins/1600km2/split/watershed_53.shp data/memorytest/dem/watershed_53.tif -32768


    python3 code/temp/memorytest.py national/Swedish1mDEM_old/mosaic1m.vrt /data/isobasins/800km2/watershed_308.shp data/memorytest/dem/watershed_308.tif -32768

    **breach test**
    python3 code/preprocess.py /temp/ /data/memorytest/dem/ /data/clipditches/ /data/clipculverts/ /data/cliproads/ /data/cliprailroads/ /data/clipstreams/ /data/memorytest/breached/

    **dtw test**
    python3 /code/temp/dtw.py /data/inspect/ /data/memorytest/dem/ /data/memorytest/breached/ 100000 /data/dtw/


## Create isobasins
80 000 grid cells equals to 200 km<sup>2</sup>

    python3 code/isobasins.py /temp/ /data/dem50m/dem_50m.tif /data/smhi/havsomraden2008_swe.shp 40000 /data/isobasins/isobasins.shp /data/isobasins/split_isobasins/

160 000 grid cells equals to 400 km<sup>2</sup>

    python3 code/isobasins.py /temp/ /data/dem50m/dem_50m.tif /data/smhi/havsomraden2008_swe.shp 160000 /data/isobasins/400km2/isobasins.shp /data/isobasins/400km2/split

320 000 grid cells equals to 800 km<sup>2</sup>

    python3 code/isobasins.py /temp/ /data/dem50m/dem_50m.tif /data/smhi/havsomraden2008_swe.shp 320000 /data/isobasins/800km2/isobasins.shp /data/isobasins/800km2/split/

640 000 grid cells equals to 1600 km<sup>2</sup>

    python3 code/isobasins.py /temp/ /data/dem50m/dem_50m.tif /data/smhi/havsomraden2008_swe.shp 640000 /data/isobasins/1600km2/isobasins.shp /data/isobasins/1600km2/split/

Isobasins between 1 km2 and 2030 km2

python3 code/isobasins.py /temp/ /data/dem50m/dem_50m.tif /data/smhi/havsomraden2008_swe.shp 640000 /data/isobasins/5km2to2030km2/isobasins.shp /data/isobasins/5km2to2030km2/split/


## Clip input data with isobasins



**Clip dem**

    python3 code/split_raster_by_isobasin.py temp/ national/Swedish1mDEM_old/tilessinglefolder/ national/Swedish1mDEM_old/mosaic1m.vrt data/isobasins/split_isobasins/ data/clipraster/ -32768


To do:
**Clip Ditches**


**Clip Culverts**

**Clip Roads**

    python3 code/split_vector_by_isobasins.py /data/isobasins/5km2to2030km2/split/ /data/fastighetskartan/2021-08-09/delivery/topo/fastighk/riks/vl_riks.shp /data/clipvector/roads/


**Clip Railroads**

    python3 code/split_vector_by_isobasins.py /data/isobasins/5km2to2030km2/split/ /data/fastighetskartan/2021-08-09/delivery/topo/fastighk/riks/vj_riks.shp /data/clipvector/railroads/
    
**Clip Streams**

    python3 code/split_vector_by_isobasins.py /data/isobasins/5km2to2030km2/split/ /data/fastighetskartan/2021-08-09/delivery/topo/fastighk/riks/vl_riks.shp /data/clipvector/streams/


# Preprocessing

The preprocessing is done to create a hydrologically compatible DEM and was done in x stepps. 
    1. AI detected ditch channels were burned into the DEM using Fillburn from whitebox.
    2. streams were burned across roads and railroads for a maximum of 50 meters.
    3. Road

    python3 code/preprocess.py /temp/ /data/clipraster/ /data/clipditches/ /data/clipculverts/ /data/cliproads/ /data/cliprailroads/ /data/clipstreams/ /data/breachedwatersheds/
    # krycklan
    python3 code/preprocess.py /temp/ /data/krycklan/dem/ /data/clipditches/ /data/clipculverts/ /data/cliproads/ /data/cliprailroads/ /data/clipstreams/ /data/krycklan/breacheddem/

    # Topographical modeling for hydrological features

    python3 code/Flowaccumulation.py /data/breachedwatersheds/ /data/D8pointer/ /data/D8flowaccumulation/


# test dtw

    python3 /code/temp/dtw.py /data/inspect/ /data/clipraster/ /data/breachedwatersheds/ 100000 /data/dtw/

    # krycklan
    python3 /code/temp/dtw.py /data/inspect/ /data/krycklan/dem/ /data/krycklan/breacheddem/ 100000 /data/dtw/

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


