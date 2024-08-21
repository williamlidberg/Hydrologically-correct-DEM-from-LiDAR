import os
import whitebox
import argparse
from tqdm import tqdm
wbt = whitebox.WhiteboxTools()
wbt.set_verbose_mode(True)

def main(temp_dir, accumulation_dir, flowacc_raster_stream_dir, vector_stream_dir, stream_initation_threshold):
    #for watershed in tqdm(os.listdir(accumulation_dir)):
    for watershed in os.listdir(accumulation_dir):    
        if watershed.endswith('.tif'):
            flowacc_raster = accumulation_dir + watershed
            rasterstreams = flowacc_raster_stream_dir + watershed
            vector_stream = vector_stream_dir + watershed.replace('.tif', '.shp')
            #reclass = '0.0;0' + str(stream_initation_threshold)
            reclass = '0.0;0;6000'
            wbt.reclass(
            i = flowacc_raster, 
            output = rasterstreams, 
            reclass_vals = reclass, 
            assign_mode=False
            )
            wbt.raster_to_vector_lines(
            i = rasterstreams, 
            output = vector_stream
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
    parser.add_argument('flowacc_raster_stream_dir', help='path to directory where the raster stream network grids will be stored')
    parser.add_argument('vector_stream_dir', help='path to directory where the vecor stream network grids will be stored')
    parser.add_argument('stream_initation_threshold',type=int, help='stream initation threshold in square meters')
    args = vars(parser.parse_args())
    main(**args)