# look into marshalling
import shutil
import obspython as OBS
import os
from datetime import datetime

randomizer_path = ''
destination_path = ''
seed_file_name = 'randomizer.dat'
stats_file_name = 'stats.txt'
is_active = False

# Description displayed in the Scripts dialog window
def script_description():
  return """Ori CopyStats/Seeds
            Copies the randomizer.dat and stats.txt into a location of your choosing."""

def script_properties():
    props = OBS.obs_properties_create()
    # Allows user to select the ori DE application path and the preferred destination path for the files
    OBS.obs_properties_add_path(props, "randomizer_path", 'Ori DE File Path', OBS.OBS_PATH_DIRECTORY, '', 'C:/Program Files (x86)/Steam/steamapps/common/Ori DE')
    OBS.obs_properties_add_path(props, "destination_path", 'File Destination Path', OBS.OBS_PATH_DIRECTORY, '', None)
    return props

def script_load(settings):
    global randomizer_path
    global destination_path
    
    randomizer_path = OBS.obs_data_get_string(settings, "randomizer_path")
    destination_path = OBS.obs_data_get_string(settings, "destination_path")
    OBS.script_log(OBS.LOG_INFO, '2023-03-22-17:57' )

    # set hotkey
    global hotkey_id
    hotkey_id = OBS.obs_hotkey_register_frontend(
        script_path(), "Ori CopyStats", ori_copystats_hotkey)
    hotkey_save_array = OBS.obs_data_get_array(
        settings, "oricopystats_hotkey")
    OBS.obs_data_array_release(hotkey_save_array)

def script_save(settings):
    # save hotkey
    hotkey_save_array = OBS.obs_hotkey_save(hotkey_id)
    OBS.obs_data_set_array(settings, "oricopystats_hotkey", hotkey_save_array)
    OBS.obs_data_array_release(hotkey_save_array)

def copyfiles(srcpath, destpath, filename):
    # Parses seed/stat files and stores the seed name for the files in variables
    # Then copies the file to the specified directory as long as the file doesn't already exist.
    if os.path.exists(srcpath + '\\' + filename):
        with open((srcpath + '\\' + filename), 'r', encoding='utf-8') as f:
            headers = f.readline()
        headers = headers.split("|", 1)
        headers[-1] = headers[-1].strip()
        headers0 = headers[0].split(",")
        headers1 = headers[1]
        headers = headers0
        headers.append(headers1)
        headers = (headers[-1])
        
        illegal_characters = '\/:*?"<>|'
        illegal_characters_found = False
        for char in illegal_characters:
            if char in headers:
                illegal_characters_found = True
                headers = headers.replace(char, '')
        if illegal_characters_found:
            headers = headers + 'illglchar'

    if not os.path.isfile(destpath + '\\' + headers + '-' + filename):
        shutil.copy2((srcpath + '\\' + filename) , (destpath + '\\' + headers + '-' +  filename))
    else:
        # If the stats file exists, it will copy with a timestamp appended.
        # If it is a duplicate seed name on a randomizer.dat file, the file will not be copied.
        if filename == stats_file_name:
            shutil.copy2((srcpath + '\\' + filename) , (destpath + '\\' + headers + '-' + datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p") + '-' + filename))


# Callback for the hotkey
def ori_copystats_hotkey(pressed):
    if pressed:
        copyfiles(randomizer_path, destination_path, seed_file_name)
        copyfiles(randomizer_path, destination_path, stats_file_name)
