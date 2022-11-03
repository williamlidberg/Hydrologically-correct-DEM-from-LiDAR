import argparse

def main(isobasindir, ditchdir, splitditchdir):
    for file in ditchdir:
        


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('isobasindir', help='path to isobasin directory')   
    parser.add_argument('ditchdir', help='path to dir with geopackages')     
    parser.add_argument('splitditchdir', help='path to directory with clipped culverts')
    args = vars(parser.parse_args())
    main(**args)