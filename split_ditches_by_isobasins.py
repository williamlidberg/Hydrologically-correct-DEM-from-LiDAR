import os
import glob
import argparse
from tqdm import tqdm
import utils.clip
import utils.vrt_ditches

# time python3 code/split_ditches_by_isobasins.py /temp/ /data/temp_clip/dem_tiles/ data/temp_clip/dem_05m.vrt /data/temp_clip/avr/ /data/temp_clip/dem_clipped/ -32768    
def main(tempdir, tilepath, vrtpath, isobasindir, clipdir, nodata): 
    
    print('build vrt')
    #utils.vrt_ditches.vrt(tilepath, vrtpath)

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
# import os
# import argparse
# import glob
# import pandas as pd
# import geopandas as gpd
# from pathlib import Path
# from utils import clip


# def main(tempdir, isobasindir, ditchdir, splitditchdir):
#     print('merge shapefiles into geodataframe')
#     shapefilepath = Path(ditchdir)
#     listofshapefiles = shapefilepath.glob('*.shp')
#     gdf = pd.concat([gpd.read_file(shp)
#         for shp in listofshapefiles
#         ]).pipe(gpd.GeoDataFrame)
#     gdf.to_file('/data/test.shp')
#     # print('clip geodataframe by watershed')
#     # for isobasin in os.listdir(isobasindir):
#     #     if isobasin.endswith('.shp'):
#     #         inputisobasin = isobasindir + isobasin
#     #         splitditch = splitditchdir + isobasin
#     #         clip.clip_geopandas(gdf, inputisobasin, splitditch)

        
# if __name__== '__main__':
#     parser = argparse.ArgumentParser(
#         description='Select the lidar tiles which contains training data',
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument('tempdir', help='path to temp directory') 
#     parser.add_argument('isobasindir', help='path to isobasin directory')   
#     parser.add_argument('ditchdir', help='path to dir with geopackages')     
#     parser.add_argument('splitditchdir', help='path to directory with clipped culverts')
#     args = vars(parser.parse_args())
#     main(**args)