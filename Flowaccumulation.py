import os
import whitebox
import argparse
from tqdm import tqdm
wbt = whitebox.WhiteboxTools()
wbt.set_verbose_mode(False)


def main(breacheddir, pointerdir, accumulationdir):
    for watershed in tqdm(os.listdir(breacheddir)):
        if watershed.endswith('.tif'):
            wbt.d8_pointer(
                dem = breacheddir + watershed, 
                output = pointerdir + watershed, 
                esri_pntr=False
            )

            wbt.d8_flow_accumulation(
            i = pointerdir + watershed, 
            output = accumulationdir + watershed, 
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
    parser.add_argument('breacheddir', help='preprocesseddem')     
    parser.add_argument('pointerdir', help='pointerdir')
    parser.add_argument('accumulationdir', help='accumulationdir')

    args = vars(parser.parse_args())
    main(**args)