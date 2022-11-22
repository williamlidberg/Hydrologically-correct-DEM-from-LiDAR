import os
import whitebox
wbt = whitebox.WhiteboxTools()
import argparse
import glob
import geopandas as gpd
import shutil
from tqdm import tqdm
from utils import clean_temp

def burn_culverts(tempdir, dem, culvert, output):
    wbt.vector_polygons_to_raster(
        i = culvert, 
        output = tempdir + dem.replace('.tif', 'culvert_.tif'),
        field= 'burndepth', 
        nodata=True, 
        cell_size=None, 
        base= dem
    )
    wbt.subtract(
        input1 = dem, 
        input2 = tempdir + dem.replace('.tif', 'culvert_.tif'), 
        output = output
    )

# python3 code/preprocessing.py /temp/ /data/clipraster/dem/ /data/clipraster/ditches/ /data/clipvector/streams/ /data/clipvector/roads_rail/ /data/clipvector/culverts/ /data/preprocessed/

# not all watersheds have culverts or ditches or roads
def main(tempdir, demdir, ditchdir, streamdir, railroaddir, culvertdir, breacheddir):
    for watershed in os.listdir(demdir):
        if watershed.endswith('.tif'):

            # Burn ditches into DEM 
            wbt.subtract(
                input1 = demdir + watershed, 
                input2 = ditchdir + watershed, 
                output = tempdir + watershed.replace('.tif', '_ditchburn.tif')
            )

            # Burn culverts into DEM
            dem = tempdir + watershed.replace('.tif', '_ditchburn.tif')
            culvert = culvertdir + watershed.replace('.tif', '.shp')
            culvertburned = tempdir + watershed.replace('.tif', '_culvertburn.tif')
            
            # Some watersheds do not have mapped culverts. Carry over the DEM to the next step.
            if os.path.isfile(culvert): 
                burn_culverts(tempdir, dem, culvert, culvertburned)
            else:
                print('no culverts to burn in this watershed, copying dem over to the next step', watershed)
                shutil.copy(dem, culvertburned)

            # Roads and railroads were merged into a single file before burning. This merging stepp is not covered in this code.
            # Some watersheds do not have mapped roads or streams. Carry over the culvertburneddem to the next step.
            streams = streamdir + watershed.replace('.tif', '.shp')
            railroads = railroaddir + watershed.replace('.tif', '.shp')
            roadburned = tempdir + watershed.replace('.tif', '_roadburned.tif')

            if os.path.isfile(streams) and os.path.isfile(railroads):
                wbt.burn_streams_at_roads(
                    dem = culvertburned,
                    streams = streams, 
                    roads = railroads, 
                    output = roadburned, 
                    width=50
                )            
            else:
                print('This watershed is missing streams or roads, copying dem over to the next step', watershed)
                shutil.copy(culvertburned, roadburned)
             
            # Final breaching step
            hydrologically_correct = breacheddir + watershed
            wbt.breach_depressions(
                dem = roadburned, 
                output = hydrologically_correct, 
                max_depth=2, 
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