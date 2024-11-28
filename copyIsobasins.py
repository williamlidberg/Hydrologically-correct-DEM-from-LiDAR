import os
import shutil
import argparse


def main(basins, dem, copiedDem):
    for basin in os.listdir(basins):
        if basin.endswith('.shp'):
            nameDEM = os.path.join(dem, basin.replace('.shp', '.tif'))
            nameCopiedDEM = os.path.join(copiedDem, basin.replace('.shp', '.tif'))
            shutil.copy(nameDEM, nameCopiedDEM)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('basins', help='Elizas Basins')   
    parser.add_argument('dem', help='corrected DEMs')     
    parser.add_argument('copiedDem', help='copied DEMs')     
    args = vars(parser.parse_args())
    main(**args)