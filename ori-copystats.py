import shutil

randomizer_path = 'D:\\games\\steam\\steamapps\\common\\Ori DE\\'
destination_path = 'D:\\OneDrive - InsomniacToaster\\Desktop\\OriDERando\\Seeds\\'
seed_file_name = 'randomizer.dat'
stats_file_name = 'stats.txt'

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
