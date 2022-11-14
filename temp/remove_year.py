# removes years from tiles to combine old ditch data with new dem tiles
import os
import glob
import argparse

def main(indir):
    
    for tile in os.listdir(indir):
        oldname = indir + tile
        new_name = tile[:11] + tile[16:] 
        newpathandtile = indir + tile.replace(tile, new_name)
        print(newpathandtile)
        os.rename(oldname, newpathandtile)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('indir', help='path to directory of dem tiles')     
    args = vars(parser.parse_args())
    main(**args)