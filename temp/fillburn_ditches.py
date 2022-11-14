import os
import argparse
import glob
from tqdm import tqdm
import whitebox
wbt = whitebox.WhiteboxTools()
#wbt.set_verbose_mode(False)


def main(demdir, ditchdir, fillburndir):
    demtiles = demdir + '/*/*.tif'
    listofalltiles = glob.glob(demtiles, recursive = True)
 
    for tile in tqdm(listofalltiles):
        if 'border' not in tile and 'metadata' not in tile:

                tilename = os.path.basename(tile)
                new_name = tilename[:11] + tilename[16:]
                ditch = ditchdir + new_name.replace('.tif', '.shp') 

                fillburn = fillburndir + new_name


                wbt.fill_burn(
                dem = tile, 
                streams = ditch, 
                output = fillburn
            )


    print(len(test))
    print(test[0])
if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('demdir', help='path to directory of dem tiles')     
    parser.add_argument('ditchdir', help='path to the directory ditches')
    parser.add_argument('fillburndir', help='path to directory of fillburned tiles')
    args = vars(parser.parse_args())
    main(**args)