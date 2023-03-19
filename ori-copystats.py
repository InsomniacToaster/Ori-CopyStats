# look into marshalling
import shutil
import obspython as OBS
import os
from datetime import datetime

randomizer_path = ''
destination_path = ''
seed_file_name = 'randomizer.dat'
stats_file_name = 'stats.txt'
hotkey_id = OBS.OBS_INVALID_HOTKEY_ID

# Description displayed in the Scripts dialog window
def script_description():
  return """Ori CopyStats/Seeds
            Copies the randomizer.dat and stats.txt into a location of your choosing."""

def script_properties():
    props = OBS.obs_properties_create()
    OBS.obs_properties_add_path(props, "randomizer_path", 'Ori DE File Path', OBS.OBS_PATH_DIRECTORY, '', 'C:/Program Files (x86)/Steam/steamapps/common/Ori DE')
    OBS.obs_properties_add_path(props, "destination_path", 'File Destination Path', OBS.OBS_PATH_DIRECTORY, '', None)
    return props

def script_load(settings):
    global randomizer_path
    global destination_path
    
    randomizer_path = OBS.obs_data_get_string(settings, "randomizer_path")
    destination_path = OBS.obs_data_get_string(settings, "destination_path")
    OBS.script_log(OBS.LOG_INFO, '2023-03-19-14:37' )

    # set hotkey
    global hotkey_id
    hotkey_id = OBS.obs_hotkey_register_frontend(
        script_path(), "Ori CopyStats", copystats_copy_files)
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
    # Then copies the file to the specified directory as long as the file doesn't already exist
    if os.path.exists(srcpath + '\\' + filename):
        with open((srcpath + '\\' + filename), 'r', encoding='utf-8') as f:
            headers = f.readline()
        headers=headers.strip().replace('|' , ',')
        headers=headers.split(",")
        headers = (headers[-1])

    if not os.path.isfile(destpath + '\\' + headers + '-' + filename):
        shutil.copy2((srcpath + '\\' + filename) , (destpath + '\\' + headers + '-' +  filename))
    else:
        shutil.copy2((srcpath + '\\' + filename) , (destpath + '\\' + headers + '-' +  filename + datetime.now().strftime("%Y-%m-%d_%I-%M-%S-%p")))
        
def copystats_copy_files(props):
    copyfiles(randomizer_path, destination_path, seed_file_name)
    copyfiles(randomizer_path, destination_path, stats_file_name)
