FROM osgeo/gdal:latest
RUN apt-get update
RUN apt-get update && apt-get install -y python3-pip


RUN pip install whitebox==2.0.3
RUN pip install rtree==1.0.1 
RUN pip install pygeos==0.13
RUN pip install geopandas==0.12.1 
RUN pip install tqdm==4.64.1 
RUN pip install rasterio==1.3.3

RUN mkdir /temp/

