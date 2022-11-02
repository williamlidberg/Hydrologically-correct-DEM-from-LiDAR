# script by william lidberg
import os
import argparse
from tqdm import tqdm
import whitebox
wbt = whitebox.WhiteboxTools()
wbt.set_verbose_mode(True)
parser = argparse.ArgumentParser(description = 'Calculates depth to water from dem. ')

# how to run
# python G:/TRISTIAN/Depth_to_water.py G:/TRISTIAN/DEM/, R:/Temp/, G:/TRISTIAN/clip_prop_streams/, G:/TRISTIAN/clip_prop_roads/, 100000, G:/TRISTIAN/depth_to_water/
class Depth_to_water:
    def __init__(self, temp_dir):
        self.temp_dir = temp_dir

    # def pre_process_breaching(self, f, dem_dir):
    #     wbt.breach_depressions(
    #         dem = dem_dir + f,
    #         output = temp_dir + 'corrected' + f,
    #         max_depth=None,
    #         max_length=None,
    #         flat_increment=0.01,
    #         fill_pits=True
    #     )

    def extract_streams(self, f, dem_dir, stream_initation_threshold):
        wbt.d8_pointer(
            dem = dem_dir + f,
            output = self.temp_dir + 'pointer' + f,
            esri_pntr=False
        )
        wbt.d8_flow_accumulation(
            i = self.temp_dir + 'pointer' + f,
            output = self.temp_dir + 'accumulation' + f,
            out_type='cells',
            log=False,
            clip=False,
            pntr=True,
            esri_pntr=False
        )
        wbt.extract_streams(
            flow_accum = self.temp_dir + 'accumulation' + f, 
            output = self.temp_dir + 'streams' + f, 
            threshold = stream_initation_threshold, 
            zero_background=True
        )

    def depth_to_water(self, f, original_dem_dir, depth_to_water_dir):
        wbt.slope(
            dem = original_dem_dir + f, 
            output = self.temp_dir + 'slope' + f, 
            zfactor=None, 
            units="radians"
        )
        wbt.tan(
            i = self.temp_dir + 'slope' + f, 
            output = self.temp_dir + 'tan' + f
        )

        wbt.cost_distance(
            source = self.temp_dir + 'streams' + f, 
            cost = self.temp_dir + 'tan' + f, 
            out_accum = depth_to_water_dir + f, 
            out_backlink = self.temp_dir + 'backlink' + f
        )

    def clean_temp_dir(self):
        for i in os.listdir(self.temp_dir):
            os.remove(self.temp_dir + i)


def main(temp_dir, original_dem_dir, breached_dem_dir, stream_initation_threshold, depth_to_water_dir):
    dtw = Depth_to_water(temp_dir)    
    for f in tqdm(os.listdir(breached_dem_dir)):
        if f.endswith('.tif'):
            dtw.extract_streams(f, breached_dem_dir, stream_initation_threshold)
            dtw.depth_to_water(f, original_dem_dir, depth_to_water_dir)
            #dtw.clean_temp_dir()
    

       
if __name__== '__main__':
    parser = argparse.ArgumentParser(
        description='Select the lidar tiles which contains training data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('temp_dir', help='path to temporary directory located on RAM disk')    
    parser.add_argument('original_dem_dir', help='Path directory of dem files')
    parser.add_argument('breached_dem_dir', help='Path directory of dem files')  
    parser.add_argument('stream_initation_threshold', type= int, help='stream_initation_threshold in square meters')  
    parser.add_argument('depth_to_water_dir', help='directory for depth to water output') 
    args = vars(parser.parse_args())
    main(**args)