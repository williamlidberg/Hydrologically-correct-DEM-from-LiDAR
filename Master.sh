#!/bin/bash 
echo "Creating isobasins"

#docker run --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest python3 code/create_isobasins.py /temp/ /data/dem50m/dem_50m.tif /data/smhi/havsomraden2008_swe.shp 640000 /data/isobasins/isobasins.shp /data/isobasins/split/

echo "Clipping DEM with Isobasins"

docker run --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest python3 code/split_raster_by_isobasins.py temp/ /national/Swedish1mDEM_old/tiles/ /national/Swedish1mDEM_old/mosaic1m.vrt data/isobasins/split_isobasins/ data/clipraster/dem/ -32768

echo "Reclassifying ditches"

#docker run --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest python3 code/reclassify_ditches.py /national/ditches/1m/probability/ /data/reclassified_ditches/

echo "Clip Ditches with Isobasins"

docker run --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest python3 code/split_ditches_by_isobasins.py /temp/ /data/reclassified_ditches/ /data/ditches1m.vrt /data/isobasins/split/ /data/clipraster/ditches/ -32768

echo "clip streams with Isobasins"

docker run --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest python3 code/split_vector_by_isobasins.py /data/isobasins/split/ /data/fastighetskartan/2021-08-09/delivery/topo/fastighk/riks/vl_riks.shp /data/clipvector/streams/

echo "Clip roads and railroads with Isobasins"

docker run --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest python3 code/split_vector_by_isobasins.py /data/isobasins/split/ /data/fastighetskartan/2021-08-09/roads_railroads.shp /data/clipvector/roads_rail/

echo "Clip culverts with Isobasins"

#docker run --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest python3 code/split_geopackage_by_isobasins.py /data/isobasins/split/ /data/culverts/ /data/clipvector/culverts/

echo "Pre-process DEM"
#docker run --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest

echo "Done"