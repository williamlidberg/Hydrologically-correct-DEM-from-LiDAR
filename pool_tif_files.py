import os
import glob
import shutil

original_dir = 'W:/lm/hojddata1m/raster/epsg3006/cumulative_2022-10-06/delivery/'
out_dir = 'Y:/national_datasets/Swedish1mDEM_old/tilessinglefolder/'
list_laz_files = glob.glob('W:/lm/hojddata1m/raster/epsg3006/cumulative_2022-10-06/delivery/**/**/*.tif', recursive = True)

non_border = []
for i in list_laz_files:
    if 'density' not in i:
        filename = os.path.basename(i)
        out = out_dir + filename
        shutil.copy(i, out)
        print('copied ', i)



# from os import listdir
# from os.path import join
# from shutil import copy
# from concurrent.futures import ThreadPoolExecutor
# import glob
# # copy a file from source to destination
# def copy_file(path, dest_dir):
#     # copy source file to dest file
#     dest_path = dest_dir + path
#     # report progress
#     print(f'.copied {path} to {dest_path}')
 
# # copy files from src to dest
# def main():
#     original_dir = 'W:/lm/hojddata1m/raster/epsg3006/cumulative_2022-10-06/delivery/'
#     dest = 'Z:/hydrologically_correct_dem/tiles1m/'
#     list_laz_files = glob.glob('W:/lm/hojddata1m/raster/epsg3006/cumulative_2022-10-06/delivery/**/**/*.tif', recursive = True)
#     # create the thread pool
#     with ThreadPoolExecutor(63) as exe:
#         # submit all copy tasks
#         _ = [exe.submit(copy_file, dest) for path in list_laz_files]
#     print('Done')
 
# # entry point
# if __name__ == '__main__':
#     main()