import os
import whitebox
wbt = whitebox.WhiteboxTools()
import argparse
import geopandas as gpd
import shutil
import rasterio
from rasterio import features
from tqdm import tqdm
from utils import clean_temp

def burn_culverts(tempdir, dem, culvert, output):

    # Due to a bug in whiteboxtools this method is not used now.
    # Instead rasterio is used to rasterize the culvert polygons. 
    # wbt.vector_polygons_to_raster(
    #     i = culvert, 
    #     output = dem.replace('_ditchburn.tif', '_culvert.tif'),
    #     field= 'burndepth', 
    #     nodata=False, 
    #     cell_size=None, 
    #     base= dem
    # )

    # This is a temporary solution using rasterio that solves the same problem
    vectorculvert = gpd.read_file(culvert)
    culvert_geometries = [shapes for shapes in vectorculvert.geometry]
    basefile = rasterio.open(dem)
    rasterized = features.rasterize(culvert_geometries,
        out_shape = basefile.shape,
        fill = 0,
        out = None,
        transform = basefile.transform,
        all_touched = False,
        default_value = 2,
        dtype = None)


    # Write to TIFF
    kwargs = basefile.meta
    kwargs.update(
        dtype=rasterio.float32,
        count=1,
        compress='lzw')
    outtile = dem.replace('_ditchburn.tif', '_culvert.tif')
    with rasterio.open(outtile, 'w', **kwargs) as dst:
        dst.write_band(1, rasterized.astype(rasterio.float32))

    # "Burn culverts into DEM by subtracting them from the DEM with 2 m"
    wbt.subtract(
        input1 = dem, 
        input2 = dem.replace('_ditchburn.tif', '_culvert.tif'), 
        output = output
    )


# not all watersheds have culverts or ditches or roads
def main(tempdir, demdir, ditchdir, streamdir, railroaddir, culvertdir, breacheddir):
    for watershed in os.listdir(demdir):
        if watershed.endswith('.tif'):
            
            # Roads and railroads were merged into a single file before burning. This merging stepp is not covered in this code.
            # Some watersheds do not have mapped roads or culverts. Carry over the ditchburned dem to the next step.
            dem = demdir + watershed
            culvert = culvertdir + watershed.replace('.tif', '.shp')
            railroads = railroaddir + watershed.replace('.tif', '.shp')
            culvertburned = tempdir + watershed.replace('.tif', '_culvertburn.tif')
            
            # Burn culverts across roads
            if os.path.isfile(culvert):
                wbt.burn_streams_at_roads(
                    dem = dem,
                    streams = culvert, 
                    roads = railroads, 
                    output = culvertburned, 
                    width=50
                )
            else:
                print(watershed, 'is missing culverts, forwarding ditchburned dem to the next step')
                shutil.copy(dem, culvertburned)

            # Roads and railroads were merged into a single file before burning. This merging stepp is not covered in this code.
            # Some watersheds do not have mapped roads or streams. Carry over the culvertburneddem to the next step.
            streams = streamdir + watershed.replace('.tif', '.shp')
            railroads = railroaddir + watershed.replace('.tif', '.shp')
            roadburned = tempdir + watershed.replace('.tif', '_roadburned.tif')
            # Burn streams across roads
            if os.path.isfile(streams) and os.path.isfile(railroads):
                wbt.burn_streams_at_roads(
                    dem = culvertburned,
                    streams = streams, 
                    roads = railroads, 
                    output = roadburned, 
                    width=50
                )            
            else:
                print(watershed, 'is missing streams or roads, forwarding the culvertburned dem to the next step')
                shutil.copy(culvertburned, roadburned)
             
            # Final breaching step
            hydrologically_correct = breacheddir + watershed
            wbt.breach_depressions(
                dem = roadburned, 
                output = hydrologically_correct, 
                max_depth=None, 
                max_length=None, 
                flat_increment=0.001, 
                fill_pits=True
            )
            clean_temp.clean(tempdir)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tempdir', help='path to ramdisk')     
    parser.add_argument('demdir', help='path to the directory of 50 m dem')
    parser.add_argument('ditchdir', help='path to a shapefile of the coastline')
    parser.add_argument('streamdir', help='path to output isobasin shapefile')
    parser.add_argument('railroaddir', help='path to output isobasin shapefile')
    parser.add_argument('culvertdir', help='path to a shapefile of the coastline')       
    parser.add_argument('breacheddir', help='path to output isobasin shapefile') 
    args = vars(parser.parse_args())
    main(**args)