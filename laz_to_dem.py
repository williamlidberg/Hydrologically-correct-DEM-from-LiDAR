# This script is affiliated with the WhiteboxTools Geospatial analysis library 
# Authors: Anthony Francioni, Carys Owens, and John Lindsay
# Created: 01/07/2020
# Adapted by William Lidberg to process swedish LiDAR data
# License: MIT

import os
import sys
sys.path.insert(1, 'C:/WhiteboxTools') #
wbt = WhiteboxTools()
#from wbt.whitebox_tools import WhiteboxTools # module call to WhiteboxTools... for more information see https://jblindsay.github.io/wbt_book/python_scripting/using_whitebox_tools.html)
from whitebox_tools import WhiteboxTools

# Function to gather the file names of TIF files and puts them in a list
def find_tif_files(input_directory): # finds TIF files in an input directory
    files = os.listdir(input_directory)
    file_names = []
    for f in files:
        if f.endswith(".tif"): #change accordingly for appropriate raster type 
            file_names.append(f)
    return file_names


def main():
    ########################
    # Set up WhiteboxTools #
    ########################
    wbt = WhiteboxTools()
    wbt.set_verbose_mode(False) # Sets verbose mode. If verbose mode is False, tools will not print output messages
    #wbt.set_compress_rasters(True) # Compressed TIF file format based on the DEFALTE algorithm
    in_directory = "E:/LAZ/ExempelBlock/19A002/" # Input file directory; change to match your environment
    output_dir = "E:/LAZ/ExempelBlock/19A002_Whitebox/" # Output file directory; change to match your environment


    wbt.set_working_dir(in_directory)
    wbt.lidar_tin_gridding(parameter="elevation", 
    returns="last", # A DEM or DTM is usually obtained from the "last" returns, a DSM uses "first" returns (or better, use the lidar_digital_surface_model tool)
    resolution=0.5, # This is the spatial resolution of the output raster in meters and should depend on application needs and point density.
    exclude_cls= "0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18", # Example of classified points to be excluded from analysis i.e. class 9 is water.
    minz=None,
    maxz=None,
    max_triangle_edge_length=50.0
    )
    print("Completed TIN interpolation \n")

    
main()
