import pandas as pd
import numpy as np

from lib.etypes import RAW_BASE_PATH, ETYPE, read_raw_dataset, append_to_tmp_dataset, exctract_and_fetch_positions, read_tmp_dataset, write_tmp_dataset
from lib.utils import check_duplicates, err, warn, info, add_id_prefix

# Base folders for GTFS datasets
FOLDERS = [
  'tt_extraurban',
  'tt_urban',

  'flixbus',

  'trenitalia/lombardia',
  'trenitalia/piemonte'
  # 'trenitalia/toscana'
]

GTFS_FILES = [
  'calendar',
  'calendar_dates',
  'routes',
  'stops',
  'stop_times',
  'trips'
]

FILENAMES = {}
for folder in FOLDERS:
  for gtfs_file in GTFS_FILES:
    FILENAMES[f'{folder}_{gtfs_file}'] = f'{RAW_BASE_PATH}{folder}/{gtfs_file}.txt'

# Loading csv files
DFS = {}
for name, path in FILENAMES.items():
  DFS[name] = pd.read_csv(path)


###################################
##                               ##
##  Calendars (Weekly Schedule)  ##
##                               ##
###################################

ws = pd.DataFrame(columns=ETYPE.WEEKLY_SCHEDULE.value['columns'])

for folder in FOLDERS:
  df = DFS[f'{folder}_calendar'].copy()
  df.rename(columns={'service_id': 'id'}, inplace=True)
  df['id'] = df['id'].astype(str)
  ws = pd.concat([ws, df])
  check_duplicates(ws, 'id')

ws = write_tmp_dataset(ETYPE.WEEKLY_SCHEDULE, ws)
print('\n\nWEEKLY SCHEDULE\n', ws)