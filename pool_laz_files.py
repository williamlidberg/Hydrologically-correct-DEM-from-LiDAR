import os
import glob
import shutil

original_dir = 'E:/LAZ/original/'
out_dir = 'E:/William/laserdataskog/pooled/'
list_laz_files = glob.glob('E:/LAZ/original/**/**/*.laz', recursive = True)

non_border = []
for i in list_laz_files:
    if 'border' not in i:
        filename = os.path.basename(i)
        out = out_dir + filename
        shutil.copy(i, out)
