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

# HERE THERE ARE DUPLICATES check_duplicates(se, 'id')
se = write_tmp_dataset(ETYPE.SCHEDULE_EXCEPTION, se)
print('\n\nSCHEDULE EXCEPTIONS\n', se)


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

  stop_type = 'bus'
  if folder.startswith('trenitalia'):
    stop_type = 'train'

  df = add_id_prefix(df, f'pos_stop_{stop_type}_{folder}_', 'localize')
  df = add_id_prefix(df, f'stop_{stop_type}_{folder}_', 'id')

  df_stops = df[['id', 'stop_name', 'localize']].copy()
  df_stops.rename(columns={'stop_name': 'name'}, inplace=True)
  df_stops = df_stops.assign(type=stop_type)

  df_pos = df[['localize', 'stop_lat', 'stop_lon']].copy()
  df_pos.rename(columns={'localize': 'id', 'stop_lat': 'latitude', 'stop_lon': 'longitude'}, inplace=True)
  df_pos['address'] = None

  positions = pd.concat([positions.astype(df_pos.dtypes), df_pos])
  stops = pd.concat([stops.astype(df_stops.dtypes), df_stops])

check_duplicates(stops, 'id')
check_duplicates(positions, 'id')
stops = write_tmp_dataset(ETYPE.STOP, stops)
positions = write_tmp_dataset(ETYPE.POSITION, positions)
print(
  '\n\nSTOPS\n', stops,
  '\n\nSTOP POSITIONS\n', positions
)



#############################################
##                                         ##
##       Routes / Trips / TripsStops       ##
##     Routes / Journeys / JourneyStop     ##
##                                         ##
#############################################

routes = pd.DataFrame(columns=get_complete_columns_list(ETYPE.ROUTE))
journeys = pd.DataFrame(columns=get_complete_columns_list(ETYPE.JOURNEY))
journeys_stops = pd.DataFrame(columns=get_complete_columns_list(ETYPE.JOURNEY_STOP))

for folder in FOLDERS:
  df_routes = DFS[f'{folder}_routes'].copy()

  agency_id = 0
  route_type = 'bus'
  if folder.startswith('tt_'): # Trentino trasporti dataset
    # Filter only busses (exclude funivia serdagna and potentially others)
    df_routes = (df_routes.loc[df_routes['route_type'] == 3])
    agency_id = 1
  elif folder.startswith('trenitalia'):
    agency_id = 2
    route_type = 'train'
  elif folder.startswith('flixbus'):
    agency_id = 3
  else:
    raise 'Agency not found for folder: ' + folder
  
  # Assign agency and type
  df_routes = df_routes.assign(agency_id=agency_id)
  df_routes = df_routes.assign(type=route_type)

  df_routes.rename(columns={'route_id': 'id', 'agency_id': 'operated', 'route_short_name': 'short_name', 'route_long_name': 'long_name'}, inplace=True)
  for col in ['id', 'short_name']:
    if col in df_routes:
      df_routes[col] = df_routes[col].astype(str)
  df_routes = add_id_prefix(df_routes, f'route_{folder}_', 'id')
  df_routes = df_routes[routes.columns]

  df_trips = DFS[f'{folder}_trips'].copy()
  df_trips.rename(columns={'trip_id': 'id', 'route_id': 'characterized', 'service_id': 'avaiability', 'trip_headsign': 'headsign', 'direction_id': 'direction', 'wheelchair_accessible': 'accessibility'}, inplace=True)
  df_trips['id'] = df_trips['id'].astype(str)
  if 'accessibility' in df_trips:
    df_trips['accessibility'] = df_trips['accessibility'].apply(lambda x: '0' if np.isnan(x) else '1')
    df_trips['accessibility'] = df_trips['accessibility'].astype(str)
  else:
    df_trips = df_trips.assign(accessibility='NaN')
  if 'headsign' in df_trips:
    df_trips['headsign'] = df_trips['headsign'].astype(str)
  if 'direction' in df_trips:
    df_trips['direction'] = df_trips['direction'].astype(float)
  df_trips['avaiability'] = df_trips['avaiability'].astype(str)
  df_trips = add_id_prefix(df_trips, f'trip_{folder}_', 'id')
  df_trips = df_trips[journeys.columns]

  df_trips_stops = DFS[f'{folder}_stop_times'].copy()
  for k in ['trip_id', 'stop_id']:
    if k in df_trips_stops:
      df_trips_stops[k] = df_trips_stops[k].astype(str)
  df_trips_stops.rename(columns={'trip_id': 'of', 'stop_id': 'at'}, inplace=True)
  df_trips_stops = add_id_prefix(df_trips_stops, f'stop_{route_type}_{folder}_', 'at')
  df_trips_stops = add_id_prefix(df_trips_stops, f'trip_{folder}_', 'of')
  df_trips_stops['id'] = df_trips_stops.index + 1
  df_trips_stops = add_id_prefix(df_trips_stops, f'trip_stop_{folder}_')
  df_trips_stops = df_trips_stops[journeys_stops.columns]

  routes = pd.concat([routes.astype(df_routes.dtypes), df_routes])
  journeys = pd.concat([journeys.astype(df_trips.dtypes), df_trips])
  journeys_stops = pd.concat([journeys_stops.astype(df_trips_stops.dtypes), df_trips_stops])

check_duplicates(routes, 'id')
check_duplicates(journeys, 'id')

routes = write_tmp_dataset(ETYPE.ROUTE, routes)
journeys = write_tmp_dataset(ETYPE.JOURNEY, journeys)
journeys_stops = write_tmp_dataset(ETYPE.JOURNEY_STOP, journeys_stops)

print(
  '\n\nROUTES\n', routes,
  '\n\nJOURNEYS\n', journeys,
  '\n\nJOURNEY STOPS\n', journeys_stops
)