FROM osgeo/gdal:latest
RUN apt-get update
RUN apt-get update && apt-get install -y python3-pip

#ARG DEBIAN_FRONTEND=noninteractive
#ENV TZ=Europe/Moscow
#RUN apt-get install -y tzdata
# RUN pip install rasterio
# RUN pip install tifffile
RUN pip install whitebox==2.0.3
# added to install splitraster witout numpy version conclict
RUN pip install rtree==1.0.1 
RUN pip install pygeos==0.13
RUN pip install geopandas==0.12.1 
RUN pip install tqdm==4.64.1 
RUN pip install rasterio==1.3.3
# RUN pip install splitraster


# # setup GDAL
# RUN apt-get install -y software-properties-common
# RUN add-apt-repository ppa:ubuntugis/ppa && apt-get update
# RUN apt-get install -y gdal-bin
# RUN apt-get install -y libgdal-dev
# RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
# RUN export C_INCLUDE_PATH=/usr/include/gdal
# RUN pip install GDAL
