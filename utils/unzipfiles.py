import os
import shutil
import argparse

# python G:\geoint\github\GeoInt\download_culverts.py D:/data/trummor/
def main(trumm_dir):

    for f in os.listdir(trumm_dir):
            if f.endswith('.zip'):
                zipfile = trumm_dir + f
                shutil.unpack_archive(zipfile, trumm_dir)
                print('unpacked ' + f)
 
if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('trumm_dir', help='path to the directory of all lidar files') 
    args = vars(parser.parse_args())
    main(**args)