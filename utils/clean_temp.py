import os

def clean(tempdir):
    for i in os.listdir(tempdir):
        os.remove(tempdir + i)