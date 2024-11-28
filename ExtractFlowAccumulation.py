import os
import argparse
import whitebox
wbt = whitebox.WhiteboxTools()

def main(pointFile, flowacc, snapped):
    for point in os.listdir(pointFile):
        if point.endswith('.shp'):
            namePointFile = os.path.join(pointFile, point)
            nameFlowAcc = os.path.join(flowacc, point.replace('.shp','.tif'))
            nameSnapped = os.path.join(snapped, point)
            wbt.snap_pour_points(
                pour_pts= namePointFile, 
                flow_accum = nameFlowAcc, 
                output = nameSnapped, 
                snap_dist = 10)
            
            # Extract values to points
            wbt.extract_raster_values_at_points(
                inputs = nameFlowAcc, 
                points = nameSnapped, 
                out_text=False)


if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('pointFile', help='Elizas Points')   
    parser.add_argument('flowacc', help='flowacc D8')     
    parser.add_argument('snapped', help='snapped points with extracted flowacc')     
    args = vars(parser.parse_args())
    main(**args)