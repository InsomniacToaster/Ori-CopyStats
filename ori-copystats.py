# look into marshalling
import shutil
import obspython as OBS

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
    OBS.script_log(OBS.LOG_INFO, randomizer_path)
    OBS.script_log(OBS.LOG_INFO, destination_path)

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

def copystats_copy_files():

    # Parses the seed and stat files and stores the 
    # seed name for the files in variables.

    with open((randomizer_path + '\\' + seed_file_name), 'r', encoding='utf-8') as f:
        seed_headers = f.readline()
    seed_headers=seed_headers.strip().replace('|' , ',')
    seed_headers=seed_headers.split(",")
    seed_headers = (seed_headers[-1])

    with open((randomizer_path + '\\' + stats_file_name), 'r', encoding='utf-8') as f:
        stats_headers = f.readline()
    stats_headers=stats_headers.strip().replace('|' , ',')
    stats_headers=stats_headers.split(",")
    stats_headers = (stats_headers[-1])

    ## Copy the seeds and stats to the specified directory
    shutil.copy2((randomizer_path + '\\' + seed_file_name) , (destination_path + '\\' + seed_headers + '-' +  seed_file_name))
    shutil.copy2((randomizer_path + '\\' + stats_file_name) , (destination_path + '\\' + stats_headers + '-' + stats_file_name))

