import glob
from osgeo import gdal

# non_border = []
# for i in list_laz_files:
#     if 'border' not in i:
#         filename = os.path.basename(i)
#         out = out_dir + filename
#         shutil.copy(i, out)
#         print('copied ', i)

def vrt(inputdir, output_vrt):
    gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')
    pathtotiles = inputdir + '/*.tif'  
    listoftiles = glob.glob(pathtotiles)
    vrt_options = gdal.BuildVRTOptions(resampleAlg='near', addAlpha=False)
    gdal.BuildVRT(output_vrt, listoftiles, options=vrt_options)