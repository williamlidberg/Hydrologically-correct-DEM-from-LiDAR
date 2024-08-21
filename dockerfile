FROM tensorflow/tensorflow:2.16.1-gpu
RUN apt-get update

# setup GDAL
RUN apt-get install libgdal-dev -y
RUN pip install GDAL==3.3.2
RUN pip install whitebox-workflows
RUN pip install whitebox
RUN pip install rasterio
RUN pip install rtree
RUN pip install pygeos
RUN pip install geopandas
RUN pip install tqdm
RUN pip install rasterio

RUN mkdir /temp/

