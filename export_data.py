# takes in a mp4 file made of 6 1280x720 video frames stiched together
# and a json file with containing time stamps
# parses the json and cuts the video at the coresponding time stamps
# exports each individual video frame for each time stamp 

import os.path
import json
import sys
import re

from pynput.keyboard import Key, Listener #for key press
import threading

global stop_export
stop_export = False

# Main export function
def main():
    global stop_export

    if not len(sys.argv) == 2:
        print("File name expected as command line argument")
        exit()

    filename = sys.argv[1]

    # expects mp4 files to be in the static directory 
    # and of the form 'participant_number'_zed_trimmed.mp4
    json_file_name = filename.replace('.mp4','_dataset.json')
    video_path = filename
    if os.path.exists(json_file_name):
        json_file = open(json_file_name, "r")
        label_data = json.load(json_file)
        p_num = filename[filename.rfind('/')+1:].split('_')[0]
        export_path = 'export/p' + p_num

        if not os.path.exists(export_path):
            os.makedirs(export_path)
        
        if os.path.exists(video_path):
            for label_key in label_data:

                if stop_export:
                    exit()
                
                time_in = float(label_data[label_key][1]) / 1000 # convert ms to second
                time_out = float(label_data[label_key][2]) / 1000 - time_in
                label = label_data[label_key][3].replace(" ", "_" )
                label_type = label_data[label_key][0]
                label_type_abr = label_type[0]
                if label_type.lower() == 'event': #e=emotion, a=action, s=speech, v=event
                    label_type_abr = 'v'

                for ind in range(1,7): #Cameras

                    if stop_export:
                        exit()
                    
                    # used for splitting the camera frames
                    row = int((ind - 1) / 2)
                    col = (ind + 1) % 2
                    x = 1280 * (col + 1)
                    y = 720 * row
                
                    output_vid = export_path + '/' + label_type_abr + '_' + label +'_cam' + str(ind) + '_'  + str(time_in) + '.mp4'
                    
                    if not os.path.isfile(output_vid):
                        cmd = 'ffmpeg -ss ' + str(time_in) + ' -i ' + video_path + ' -strict -2 -t ' + str(time_out) +  ' -filter:v "crop=1280:720:' + str(x) + ':' + str(y) + '" ' + output_vid
                        os.system(cmd)

# Key press listener
def on_press(key):
    global stop_export
    if key == Key.esc:
        stop_export = True
        exit()

if __name__ == "__main__":

    # Use thread so we can press ESCAPE key to cancel
    t = threading.Thread(target=main)
    t.start()
    
    # Keybooard key listener
    with Listener(on_press=on_press) as listener: listener.join()

