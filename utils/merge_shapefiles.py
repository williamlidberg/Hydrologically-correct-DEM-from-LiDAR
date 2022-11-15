import argparse
import geopandas as gpd
def merge(shape1, shape2):
    line1 = gpd.read_file(shape1)
    line2 = gpd.read_file(shape2)
    

if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('probabilitydir', help='path to probability tiles')   
    parser.add_argument('reclassifieddir', help='path to dir with reclassified ditches')     
    args = vars(parser.parse_args())
    main(**args)