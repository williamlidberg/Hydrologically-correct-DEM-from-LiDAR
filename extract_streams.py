import os
import whitebox
import argparse
from tqdm import tqdm
wbt = whitebox.WhiteboxTools()
wbt.set_verbose_mode(False)


def main(temp_dir, accumulation_dir, d8_pointer_dir, raster_stream_dir, vector_stream_dir, stream_initation_threshold):
    for watershed in tqdm(os.listdir(accumulation_dir)):
    #for watershed in os.listdir(accumulation_dir):    
        if watershed.endswith('.tif'):
            wbt.extract_streams(
                flow_accum = accumulation_dir + watershed, 
                output = temp_dir + watershed, 
                threshold = stream_initation_threshold, 
                zero_background=True
            )
            wbt.hack_stream_order(
                d8_pntr = d8_pointer_dir + watershed, 
                streams = temp_dir + watershed, 
                output = raster_stream_dir + watershed, 
                esri_pntr=False, 
                zero_background=True
            )
            wbt.raster_streams_to_vector(
                streams = raster_stream_dir + watershed, 
                d8_pntr = d8_pointer_dir + watershed, 
                output = vector_stream_dir + watershed.replace('.tif', '.shp'), 
                esri_pntr=False
            )
            if os.path.exists(temp_dir + watershed):
                os.remove(temp_dir + watershed)
            else:
                print("The file does not exist") 

if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('temp_dir', help='path to temporary directory.')
    parser.add_argument('accumulation_dir', help='path to directory where the flow accumulation are stored')
    parser.add_argument('d8_pointer_dir', help='path to directory where the flow pointer gridsa are stored')
    parser.add_argument('raster_stream_dir', help='path to directory where the raster stream network grids will be stored')
    parser.add_argument('vector_stream_dir', help='path to directory where the vecor stream network grids will be stored')
    parser.add_argument('stream_initation_threshold',type=int, help='stream initation threshold in square meters')
    args = vars(parser.parse_args())
    main(**args)