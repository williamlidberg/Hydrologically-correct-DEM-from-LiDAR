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



# not all watersheds have culverts or ditches or roads. compare lists between each?

def main(tempdir, demdir, streamdir, railroaddir culvertdir, ditchdir,, , breacheddir):
    for watershed in os.listdir(demdir):
        if watershed.endswith('.tif'):


            # Roads and railroads were merged into a single file before burning.
            roadburned = tempdir + watershed.replace('.tif', '_roadburned.tif')
            dem = tempdir + watershed
            wbt.burn_streams_at_roads(
                dem = dem,
                streams = streamdir + watershed.replace('.tif', '.shp'), 
                roads = railroaddir + watershed.replace('.tif', '.shp'), 
                output = roadburned, 
                width=50
            )            
            


            # Burn culverts into DEM
            dem = tempdir + watershed.replace('.tif', '_roadburned.tif')
            culvert = culvertdir + watershed.replace('.tif', '.shp')
            burned = tempdir + watershed.replace('.tif', '._culvertburn.tif')
            burn_culverts(tempdir, dem, culvert, burned)


            # Burn ditches into DEM 
            wbt.subtract(
                input1 = tempdir + watershed.replace('.tif', '._culvertburn.tif'), 
                input2 = ditchdir + watershed, 
                output = tempdir + watershed.replace('.tif', '._ditchburn.tif')
            )


            # some watersheds do not have mapped culverts. Carry over the DEM to the next step.
            if roadburned not in os.listdir(tempdir):
                print('no road burned dem in temp dir, copying dem over', watershed)
                dem = dem + watershed
                copydem = tempdir + watershed.replace('.tif', '_roadburned.tif')
                shutil.copy(dem, copydem)

            
            # Final breaching step
            wbt.breach_depressions(
                dem = tempdir + watershed.replace('.tif', '._ditchburn.tif'), 
                output = breacheddir + watershed, 
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
    parser.add_argument('culvertdir', help='path to a shapefile of the coastline')
    parser.add_argument('roaddir', help='target size of isobasins in int values')
    parser.add_argument('railroaddir', help='path to output isobasin shapefile')
    parser.add_argument('streamdir', help='path to output isobasin shapefile')  
    parser.add_argument('breacheddir', help='path to output isobasin shapefile') 
    args = vars(parser.parse_args())
    main(**args)