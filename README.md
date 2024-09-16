[![docs](https://img.shields.io/badge/whitebox-docs-brightgreen.svg)](https://www.whiteboxgeo.com/manual/wbt_book/preface.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![docker image](https://img.shields.io/docker/pulls/williamlidberg/ditchnet.svg)](https://hub.docker.com/repository/docker/williamlidberg/ditchnet)
[![Twitter Follow](https://img.shields.io/twitter/follow/William_Lidberg?style=social)](https://twitter.com/william_lidberg)

# Hydrologicall-correct-DEM-1m

<img src="images/breached.png" alt="Charcoal kiln" width="100%"/>

# Table of  Contents

1. [Introduction](#Introduction)
2. [Data](#Data)
    1. [Digital elevation model](##Digital-elevation-model)
    1. [Ditches](##Ditches)
    1. [Road culverts](##Road-culverts)
    1. [Roads, Railroads and streams](##Roads,-Railroads-and-streams)
3. [Docker container](##Docker-container)
4. [Run pre-processing](#Run-pre-processing)
    1. [Create isobasins](##Create-isobasins)
    1. [Clip raster data with isobasins](##Clip-raster-data-with-isobasins)
    1. [Clip vector data with isobasins](##Clip-vector-data-with-isobasins)
5. [Pre-processing method](#Pre-processing-method)
6. [Streams](#Streams)
    1. [Flow pointer](#Flow-pointer)
    1. [Flow accumulation](#Flow-accumulation)
    1. [Define streams](#Define-streams)



***
# Introduction
With the introduction of high-resolution digital elevation models, it is possible to use digital terrain analysis to extract small streams. In order to map streams correctly, it is necessary to remove errors and artificial sinks in the digital elevation models. This step is known as preprocessing and will allow water to move across a digital landscape. However, new challenges are introduced with increasing resolution because the effect of anthropogenic artefacts such as road embankments and bridges increases with increased resolution. These are problematic during the preprocessing step because they are elevated above the surrounding landscape and act as artificial dams. 

Sinks are defined as areas surrounded by cells with higher elevations, which prevent water from moving further. Thus, preprocessing of DEMs is important, especially because any errors in the input data will be amplified with each subsequent calculation. There are two commonly used methods to handle sinks: filling and breaching. A fill algorithm examines the cells surrounding a sink and increases the elevation of the sink cells to match the lowest outlet cell. A breaching algorithm instead lowers the elevation of cells along a path between the lowest cell in the sink and the outlet of the sink. This project will be build on the work by [Lidberg et al 2017](https://onlinelibrary.wiley.com/doi/10.1002/hyp.11385) and [Lidberg et al 2021](fixlink) by burning ditches and culverts into the DEM.

# Data
## Digital elevation model
 
 The digital elevation model (DEM) had a resolution of 1 m and were downloaded by SLU. This data was a mix of the old LiDAR scan and the new LiDAR scan known as "laserdata skog nedladdning". It was stored under the **/national/Swedish1mDEM_old/tiles/** directory. A DEM resampled to 50x50m was used to create the watersheds or isobasins. It was stored under
**/data/dem50m/**

## Ditches
The ditches used for this project was created with the AI model described by xxxx. The ditch probability raster was used to burn in ditches into the DEM. The ditches were stored under **/national/ditches/1m/probability/**

## Road culverts
Culverts were downloaded as geopackages from the [Swedish traffic authority](https://lastkajen.trafikverket.se/login). The culvert data were stored in **/data/culverts/**

## Roads, Railroads and streams

Railroads, road and stream networks were extracted from the swedish property map created by [Swedish traffic authority](https://www.lantmateriet.se/). They were stored as lines that covered all of Sweden. The data were stored under **/data/fastighetskartan/2021-08-09/delivery/topo/fastighk/riks/**

# Docker container
A gdal docker image was used as a base for this project and the following python packages were installed: whitebox, rtree, pygeos, geopandas, tqdm, rasterio. Refer to the dockerfile for details on versions and environment setup. A complete docker image can be pulled from xxxx

The data from our servers were mounted to the container over a 10 GBit network:\
**data** is the general directory where all the processing were done.\
**temp** is a local drive where intermediate files were written to avoid reading and writing large amounts of data over the network. I suggest that this drive consists of a RAM disk or at least a fast SSD\
**national** is where the 1 m DEM tiles were located. This directroy was mounted seperatly to avoid moving large amounts of data to the "data" directory.\
**code** is a local github repository
\
\
Navigate to the dockerfile and build container. In my case this was done like this:

    cd /mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/
    docker build -t dem .

    
# Run pre-processing


This is an example on how to run the container in interactive mode: 
 
    docker run -it  --mount type=bind,source=/mnt/GIS/hydrologically_correct_dem_1m/,target=/data --mount type=bind,source=/mnt/Extension_100TB/national_datasets/,target=/national --mount type=bind,source=/mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR/,target=/code --mount type=bind,source=/mnt/ramdisk/,target=/temp dem:latest   

## Isobasins
The 1 m DEM was to large to be processed as one single file. Therefore it was split into smaller areas. This split was done using nearly equal-sized watersheds known as isobasins. The isobasins were extracted from a 50 m DEM using the script [create_isobasins.py](create_isobasins.py) which was based on [Whitebox Tools](https://www.whiteboxgeo.com/manual/wbt_book/available_tools/hydrological_analysis.html?highlight=isobasins#isobasins).

## Clip raster data with isobasins
The raster data **DEM** and **ditches** were stored as 2.5 km tiles so they were first stored as viritual mosaics before being clipped by the isobasin polygons. The ditches were in the form of probability of a pixel being a ditch as described in [Lidberg et al 2022](https://github.com/williamlidberg/Mapping-drainage-ditches-in-forested-landscapes-using-deep-learning-and-aerial-laser-scanning). The pixel values were [reclassified](reclassify_ditches.py) in order to be used to burn ditch channels into the DEM. For example If the probability of a pixel being part of a ditch was 60 % it were burned into the DEM by 60 cm. If the probability were 100% it were burned into the DEM by 100 cm. 

## Clip vector data with isobasins
Roads, railroads and streams from the swedish property map were clipped with isobasins using the script [split_vector_by_isobasins.py](split_vector_by_isobasins.py) while culverts were stored as geopackage and were instead clipped using [split_geopackage_by_isobasins.py](split_geopackage_by_isobasins.py)

## Clip AI-predicted culverts by isobasins
    docker run -it --rm -v /mnt/qnap2/william/projects/hydroDEM/$:/data -v /mnt/qnap2/william/projects/culverts/data/inference/sweden/:/culverts -v /mnt/Extension_100TB/William/GitHub/Hydrologically-correct-DEM-from-LiDAR:/code dem:latest
        
    python code/clipShapeDirByIsobasins.py /data/split/ /culverts/vector/ /data/clipvector/DeepBreach/




# Pre-processing method

The pre-processing is done to create a hydrologically compatible DEM and was done in five stepps:

    1. The ditch probabiity channels were burned into the DEM.
    2. streams and culverts were burned across roads and railroads for a maximum of 50 meters.
    3. Single cell pits were filled
    4. Completly flat areas such as lakes were given a slope of 0.001 degrees
    5. All remaining depressions/sinks were resolved by an agressive breaching approach

Script

    python3 /code/preprocess.py /temp/ /data/clipraster/dem_test/ /data/clipraster/ditches/ /data/clipVector/streams/ /data/clipVector/roads_rail/ /data/clipVector/culverts_line/ /data/clipVector/deepBreach/ /data/HydrologicallyCorrectDEM/


# Flow pointer and Flow accumulation
    python3 /code/flow_accumulation.py /data/preprocessed/ /data/d8_flow_pointer/ /data/d8_flow_accumulation/

# Streams
Streams are extracted from flow accumulation rasters based on the hydrologicall compatible DEM. The flow accumulation algorithm accepts both a DEM or flow pointer grid as input. Since the flow pointer grid is usefull for many other tasks it will be extracted along side the flow accumulation. The script "flow_accumulation.py" takes the pre-processed DEM as input and will output both flow pointer and flow accumulation rasters

## Extract streams 05 ha

    python3 /code/extract_streams.py /temp/ /data/temp_flowacc/ /data/temp_flowdirr/ /data/d8_raster_streams_05ha/ /data/d8_vector_streams_05ha/ 5000


## Extract streams 1 ha

    python3 /code/extract_streams.py /temp/ /data/d8_flow_accumulation/ /data/d8_flow_pointer/ /data/d8_raster_streams_1ha/ /data/d8_vector_streams_1ha/ 10000

## Extract streams 2 ha

    python3 /code/extract_streams.py /temp/ /data/d8_flow_accumulation/ /data/d8_flow_pointer/ /data/d8_raster_streams_2ha/ /data/streams_SKS/d8_vector_streams_2ha/ 20000
## Extract streams 6 ha

    python3 /code/extract_streams.py /temp/ /data/d8_flow_accumulation/ /data/d8_flow_pointer/ /data/d8_raster_streams_6ha/ /data/d8_vector_streams_6ha/ 60000


## Extract streams 10 ha
    python3 /code/extract_streams.py /temp/ /data/d8_flow_accumulation/ /data/d8_flow_pointer/ /data/d8_raster_streams_10ha/ /data/d8_vector_streams_10ha/ 100000


# Contact
Name: William Lidberg\
Mail: William.lidberg@slu.se\
Phone: 0706925567

