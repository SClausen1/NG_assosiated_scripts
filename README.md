# NG_assosiated_scripts
Python scripts and related programs for ongoing natural gesture research

# Export_data.py 
Takes a video file name (made of 6 frames stiched together) as input from the command line (for interfacing with a flask application) 
finds an assosiated json file, reads the json file (for timestamps)
Cuts the video at each timestamp and splits the video into its 6 seperate angles
then writes them to an export folder
