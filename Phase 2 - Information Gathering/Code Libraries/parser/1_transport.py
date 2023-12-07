import pandas as pd
import numpy as np

from lib.etypes import RAW_BASE_PATH, ETYPE, read_raw_dataset, append_to_tmp_dataset, exctract_and_fetch_positions, read_tmp_dataset, write_tmp_dataset, get_complete_columns_list
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
  df = add_id_prefix(df, f'ws_{folder}_', 'id')
  ws = pd.concat([ws, df])

check_duplicates(ws, 'id')
ws = write_tmp_dataset(ETYPE.WEEKLY_SCHEDULE, ws)
print('\n\nWEEKLY SCHEDULES\n', ws)



#############################################
##                                         ##
##   Calendar date (Schedule Exceptions)   ##
##                                         ##
#############################################

se = pd.DataFrame(columns=get_complete_columns_list(ETYPE.SCHEDULE_EXCEPTION))

for folder in FOLDERS:
  df = DFS[f'{folder}_calendar_dates'].copy()
  df.rename(columns={'service_id': 'id', 'exception_type': 'type'}, inplace=True)
  df = add_id_prefix(df, f'se_{folder}_', 'id')
  se = pd.concat([se, df])

check_duplicates(se, 'id')
ws = write_tmp_dataset(ETYPE.SCHEDULE_EXCEPTION, se)
print('\n\SCHEDULE EXCEPTIONS\n', se)


###################################
##                               ##
##             Stops             ##
##                               ##
###################################

positions = pd.DataFrame(columns=get_complete_columns_list(ETYPE.POSITION))
stops = pd.DataFrame(columns=get_complete_columns_list(ETYPE.STOP))

for folder in FOLDERS:
  df = DFS[f'{folder}_stops'].copy()
  df.rename(columns={'stop_id': 'id'}, inplace=True)
  df['localize'] = df['id'].astype(str)
  df = add_id_prefix(df, f'pos_stop_{folder}_', 'localize')
  df = add_id_prefix(df, f'stop_{folder}_', 'id')

  stop_type = 'bus'
  if folder.startswith('trenitalia'):
    stop_type = 'train'
  df_stops = df[['id', 'stop_name', 'localize']].copy()
  df_stops.rename(columns={'stop_name': 'name'}, inplace=True)
  df_stops = df_stops.assign(type=stop_type)

  df_pos = df[['localize', 'stop_lat', 'stop_lon']].copy()
  df_pos.rename(columns={'localize': 'id', 'stop_lat': 'latitude', 'stop_lon': 'longitude'}, inplace=True)
  df_pos['address'] = None

  positions = pd.concat([positions.astype(df_pos.dtypes), df_pos])
  stops = pd.concat([stops.astype(df_stops.dtypes), df_stops])

stops = write_tmp_dataset(ETYPE.STOP, stops)
positions = write_tmp_dataset(ETYPE.POSITION, positions)
print('\n\nSTOPS\n', stops, '\n\nPOSITIONS\n', positions)