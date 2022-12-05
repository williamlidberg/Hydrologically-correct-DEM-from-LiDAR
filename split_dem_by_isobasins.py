import os
import glob
import argparse
from tqdm import tqdm
import utils.clip
import utils.vrt_dem

    
def main(tempdir, tilepath, vrtpath, isobasindir, clipdir, nodata): 
    
    print('build vrt')
    #utils.vrt_dem.vrt(tilepath, vrtpath)


    print('clip raster to isobasin outlines')
    pathtoshapefiles = isobasindir + '/*.shp'  
    listofshapefiles = glob.glob(pathtoshapefiles)
    for basin in tqdm(listofshapefiles):
        outname = clipdir + os.path.basename(basin).replace('.shp', '.tif')
        utils.clip.clip_raster(vrtpath, basin, outname, nodata)

    print('cleaning temp dir')
    for i in tqdm(os.listdir(tempdir)):
        os.remove(tempdir + i)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('tempdir', help='path to ramdisk')   
    parser.add_argument('tilepath', help='path to directory of all tiles')     
    parser.add_argument('vrtpath', help='path and name of output vrt')
    parser.add_argument('isobasindir', help='path to the directory with split isobasins')     
    parser.add_argument('clipdir', help='path to the output directory for clipped rasters')
    parser.add_argument('nodata', help='nodatavalue of the input raster',type=int)
    args = vars(parser.parse_args())
    main(**args)