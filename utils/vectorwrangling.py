import glob
import geopandas as gpd
import pandas
from pathlib import Path


def shp_to_gpkg(shapedir, geopackage):
    shapefilepath = Path(shapedir)
    listofshapefiles = shapefilepath.glob('*.shp')
    gdf = pandas.concat([gpd.read_file(shp)
        for shp in listofshapefiles
        ]).pipe(gpd.GeoDataFrame)
    name = Path(geopackage).stem
    gdf.to_file(geopackage, layer=name, driver="GPKG")

def gpkg_to_gpkg(geopackagedir, geopackage):
    filepath = Path(geopackagedir)
    listoffiles = filepath.glob('*.gpkg')
    gdf = pandas.concat([gpd.read_file(gpkg)
        for gpkg in listoffiles
        ]).pipe(gpd.GeoDataFrame)
    name = Path(geopackage).stem
    gdf.to_file(geopackage, layer=name, driver="GPKG")