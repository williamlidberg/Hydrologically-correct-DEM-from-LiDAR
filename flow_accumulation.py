import os
import whitebox
import argparse

wbt = whitebox.WhiteboxTools()
wbt.set_verbose_mode(False)


def main(breached_dir, pointer_dir, accumulation_dir):
    for watershed in os.listdir(breached_dir):
        if watershed.endswith('.tif'):
            wbt.d8_pointer(
            dem = os.path.join(breached_dir, watershed), 
            output = os.path.join(pointer_dir, watershed), 
            esri_pntr=False
            )

            wbt.d8_flow_accumulation(
            i = os.path.join(pointer_dir, watershed), 
            output = os.path.join(accumulation_dir, watershed), 
            out_type='catchment area', 
            log=False, 
            clip=False, 
            pntr=True, 
            esri_pntr=False
            )


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('breached_dir', help='preprocessed DEM')     
    parser.add_argument('pointer_dir', help='path to directory where the flow pointer grids will be stored')
    parser.add_argument('accumulation_dir', help='path to directory where the flow accumulation grids will be stored')

    args = vars(parser.parse_args())
    main(**args)