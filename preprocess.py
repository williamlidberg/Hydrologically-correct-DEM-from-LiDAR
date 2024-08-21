import os
import whitebox
wbt = whitebox.WhiteboxTools()
import argparse
import geopandas as gpd
import shutil
from rasterio import features
from tqdm import tqdm
from utils import clean_temp

# python3 /code/preprocess.py /temp/ /data/clipraster/dem_test/ /data/clipraster/ditches/ /data/clipVector/streams/ /data/clipVector/roads_rail/ /data/clipVector/culverts_line/ /data/clipVector/deepBreach/ /data/HydrologicallyCorrectDEM/ 
# not all watersheds have culverts or ditches or roads
def main(tempdir, demdir, ditchdir, streamdir, railroaddir, culvertdir, AIculvertdir, breacheddir):
    for watershed in os.listdir(demdir):
        if watershed.endswith('.tif'):
            print('Burn ditches into DEM') 
            input1 = os.path.join(demdir, watershed)
            input2 = os.path.join(ditchdir, watershed)
            ditchburned = tempdir + watershed.replace('.tif', '_ditchburn.tif')
            wbt.subtract(
                input1 = input1,  
                input2 = input2, 
                output = ditchburned
            )
            # Burn culverts into the DEM. Two datasets with culverts were used. lines from trafikverket and AI detected culverts.
            # Some watersheds do not have mapped roads or culverts. Carry over the ditchburned dem to the next step.
            culvert = os.path.join(culvertdir, watershed.replace('.tif', '.shp'))
            railroads = os.path.join(railroaddir, watershed.replace('.tif', '.shp'))
            culvertburned = os.path.join(tempdir, watershed.replace('.tif', '_culvertburn.tif'))
            
            print('Burn trafikverket culverts across roads')
            if os.path.isfile(culvert):
                wbt.burn_streams_at_roads(
                    dem = ditchburned,
                    streams = culvert, 
                    roads = railroads, 
                    output = culvertburned, 
                    width=50
                )
            else:
                print(watershed, 'is missing culverts, forwarding ditchburned dem to the next step')
                shutil.copy(ditchburned, culvertburned)

            # Burn AI detected culverts into the DEM.
            # convert polygon to raster
            AI_culverts = os.path.join(AIculvertdir, watershed.replace('.tif', '.shp'))
            AI_culvert_raster = os.path.join(tempdir, watershed.replace('.tif', '_AI_culvert_raster.tif'))
            wbt.vector_polygons_to_raster(
            i = AI_culverts, 
            output = AI_culvert_raster, 
            field="VALUE", 
            nodata=False, 
            cell_size=None, 
            base=input1 # dem
            )   
            
            print('burn AI culverts into the DEM')
            AI_culvert_burned = os.path.join(tempdir, watershed.replace('.tif', '_AIculvertburn.tif'))
            if os.path.isfile(AI_culverts):
                wbt.subtract(
                input1 = culvertburned,
                input2 = AI_culvert_raster, 
                output = AI_culvert_burned
            )
            else:
                print(watershed, 'is missing Ai culverts, forwarding the culvertburned dem to the next step')
                shutil.copy(culvertburned, AI_culvert_burned)


            # Roads and railroads were merged into a single file before burning. This merging stepp is not covered in this code.
            # Some watersheds do not have mapped roads or streams. Carry over the culvertburneddem to the next step.
            streams = streamdir + watershed.replace('.tif', '.shp')
            railroads = railroaddir + watershed.replace('.tif', '.shp')
            roadburned = tempdir + watershed.replace('.tif', '_roadburned.tif')
            print('Burn streams across roads')
            if os.path.isfile(streams) and os.path.isfile(railroads):
                wbt.burn_streams_at_roads(
                    dem = AI_culvert_burned,
                    streams = streams, 
                    roads = railroads, 
                    output = roadburned, 
                    width=50
                )            
            else:
                print(watershed, 'is missing streams or roads, forwarding the culvertburned dem to the next step')
                shutil.copy(culvertburned, roadburned)
             
            print('Final breaching step')
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
    parser.add_argument('AIculvertdir', help='path to a shapefile of the coastline')      
    parser.add_argument('breacheddir', help='path to output isobasin shapefile') 
    args = vars(parser.parse_args())
    main(**args)