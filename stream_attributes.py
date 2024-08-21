import os
import whitebox
import argparse
from tqdm import tqdm
wbt = whitebox.WhiteboxTools()
wbt.set_verbose_mode(False)

# 
def main(d8_pointer_dir, raster_stream_dir, dem_dir, stream_slope_dir):
    for watershed in tqdm(os.listdir(raster_stream_dir)):
        if watershed.endswith('.tif'):
            wbt.stream_slope_continuous(
                d8_pntr = d8_pointer_dir + watershed, 
                streams = raster_stream_dir + watershed, 
                dem = dem_dir + watershed, 
                output = stream_slope_dir + watershed, 
                esri_pntr=False, 
                zero_background=False
            )


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('d8_pointer_dir', help='path to directory where the flow pointer gridsa are stored')
    parser.add_argument('raster_stream_dir', help='path to directory where the raster stream network grids will be stored')
    parser.add_argument('dem_dir', help='dem_dir')
    parser.add_argument('stream_slope_dir', help='stream_slope_dir')
    args = vars(parser.parse_args())
    main(**args)



