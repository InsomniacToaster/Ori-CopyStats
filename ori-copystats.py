import shutil
import obspython as S

prop_oride_path = ''
prop_destination_path = ''
randomizer_path = prop_oride_path
destination_path = prop_destination_path
seed_file_name = 'randomizer.dat'
stats_file_name = 'stats.txt'

# Description displayed in the Scripts dialog window
def script_description():
  return """Ori CopyStats/Seeds
            Copies the randomizer.dat and stats.txt into a location of your choosing."""

def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_path(props, 'prop_oride_path', 'Ori DE File Path', S.OBS_PATH_DIRECTORY, '', 'C:/Program Files (x86)/Steam/steamapps/common/Ori DE')
    S.obs_properties_add_path(props, "prop_destination_path", "File Destination Path", S.OBS_PATH_DIRECTORY, '', None)
    return props

def script_load(settings):
    prop_oride_path = S.obs_data_get_string(settings, 'prop_oride_path')
    prop_destination_path = S.obs_data_get_string(settings, 'prop_destination_path')

def copy_files():

    ## Parses the seed and stat files and stores the seed name for the files in variables.

    with open((randomizer_path + seed_file_name), 'r', encoding='utf-8') as f:
        seed_headers = f.readline()
    seed_headers=seed_headers.strip().replace('|' , ',')
    seed_headers=seed_headers.split(",")
    seed_headers = (seed_headers[-1])

    with open((randomizer_path + stats_file_name), 'r', encoding='utf-8') as f:
        stats_headers = f.readline()
    stats_headers=stats_headers.strip().replace('|' , ',')
    stats_headers=stats_headers.split(",")
    stats_headers = (stats_headers[-1])

    ## Copy the seeds and stats to the specified directory
    shutil.copy2((randomizer_path + seed_file_name) , (destination_path + seed_headers + '-' +  seed_file_name))
    shutil.copy2((randomizer_path + stats_file_name) , (destination_path + stats_headers + '-' + stats_file_name))

