import glob
from osgeo import gdal

def vrt(inputdir, output_vrt):
    gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')
    pathtotiles = inputdir + '/*.tif'  
    listoftiles = glob.glob(pathtotiles)
    vrt_options = gdal.BuildVRTOptions(resampleAlg='near', addAlpha=False)
    gdal.BuildVRT(output_vrt, listoftiles, options=vrt_options)