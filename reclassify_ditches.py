import os
import argparse
import rasterio
import numpy as np
from tqdm import tqdm

def reclass(intile, outtile):
    with rasterio.open(intile) as src:
        band1 = src.read(1)
        rescale = band1 / 100
        reclass = rescale[rescale <= 0.5] = 0
        reclass = np.array(rescale)

        # Write to TIFF
        kwargs = src.meta
        kwargs.update(
            dtype=rasterio.float32,
            count=1,
            compress='lzw')

        with rasterio.open(outtile, 'w', **kwargs) as dst:
            dst.write_band(1, reclass.astype(rasterio.float32))


def main(probabilitydir, reclassifieddir):
    for tile in tqdm(os.listdir(probabilitydir)):
        intile = probabilitydir + tile
        outtile = reclassifieddir + tile
        reclass(intile, outtile)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('probabilitydir', help='path to probability tiles')   
    parser.add_argument('reclassifieddir', help='path to dir with reclassified ditches')     
    args = vars(parser.parse_args())
    main(**args)