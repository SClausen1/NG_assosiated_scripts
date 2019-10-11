# takes in a mp4 file made of 6 1280x720 video frames stiched together
# and a json file with containing time stamps
# parses the json and cuts the video at the coresponding time stamps
# exports each individual video frame for each time stamp 

import os.path
import json
import sys
import re

def main(argv):
    
    # expects mp4 files to be in the static directory 
    # and of the form 'participant_number'_zed_trimmed.mp4
    json_file_name = 'static\\' + argv.replace('.mp4','_dataset.json')
    video_path = 'static\\' + argv
    if os.path.exists(json_file_name):
        json_file = open(json_file_name, "r")
        label_data = json.load(json_file)
        p_num = re.match("\d+", argv)
        export_path = 'export\p' + p_num[0]

        if not os.path.exists(export_path):
            os.makedirs(export_path)
        
        if os.path.exists(video_path):
            for label_key in label_data:
                
                label_type = label_data[label_key][0]
                time_in = str(float(label_data[label_key][1]) / 1000) # convert ms to second
                time_out = str(float(label_data[label_key][2]) / 1000)
                label = label_data[label_key][3].replace(" ", "_" )
                label_type_abr = label_type[0]

                if label_type == 'Event':
                    label_type_abr = 'v'

                for ind in range(1,7): #Cameras
                    
                    # used for splitting the camera frames
                    row = int((ind - 1) / 2)
                    col = (ind + 1) % 2
                    x = 1280 * (col + 1)
                    y = 720 * row
                
                    output_vid = 'export\p' + p_num[0] + '\\' + label_type_abr + '_' + label +'_cam' + str(ind) + '_'  + str(time_in) + '.mp4'
                    
                    if not os.path.isfile(output_vid):
                        cmd = 'ffmpeg -i ' + video_path + ' -ss ' + time_in + ' -strict -2 -to ' + time_out +  ' -filter:v "crop=1280:720:' + str(x) + ':' + str(y) + '" ' + output_vid
                        os.system(cmd)



if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("File name expected as command line argument")