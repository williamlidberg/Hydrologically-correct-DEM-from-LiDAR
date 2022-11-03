import glob
from osgeo import gdal


def vrt(inputdir, output_vrt):
    
    # border files needs to be excluded before creating the vrt
    pathtotiles = inputdir + '/*/*.tif'  
    listofalltiles = glob.glob(pathtotiles,recursive = True)
    listoftileswithoutborder = []
    for tile in listofalltiles:
        if 'border' not in tile and 'metadata' not in tile and 'density' not in tile:
            listoftileswithoutborder.append(tile)
    print(len(listoftileswithoutborder), 'tiles detected')
    # create vrt from none border tiles
    gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')
    vrt_options = gdal.BuildVRTOptions(resampleAlg='near', addAlpha=False)
    gdal.BuildVRT(output_vrt, listoftileswithoutborder, options=vrt_options)



# def vrt(inputdir, output_vrt):
#     gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')
#     pathtotiles = inputdir + '/*.tif'  
#     listoftiles = glob.glob(pathtotiles)
#     vrt_options = gdal.BuildVRTOptions(resampleAlg='near', addAlpha=False)
#     gdal.BuildVRT(output_vrt, listoftiles, options=vrt_options)    