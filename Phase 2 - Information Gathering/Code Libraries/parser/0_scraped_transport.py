import pandas as pd
import numpy as np

from lib.etypes import RAW_BASE_PATH, ETYPE, read_raw_dataset, append_to_tmp_dataset, exctract_and_fetch_positions, read_tmp_dataset, write_tmp_dataset, get_complete_columns_list
from lib.utils import check_duplicates, err, warn, info, add_id_prefix

SCRAPY_OUT_BASE_PATH = '../../Raw data/scraped/'
SCRAPY_BASEPATH = '../E656_scraper/Scraped data/'
SCRAPY_DFS = {}
SCRAPY_FILENAMES = {
  'trento_trains': 'trento_trains',
  'ftm_trains': 'ftm_routes_trips',
  'stops': 'stops',
  # 'ftm_stops': 'ftm_stops',
}

for name, path in SCRAPY_FILENAMES.items():
  SCRAPY_DFS[name] = pd.read_json(SCRAPY_BASEPATH + path + '.json')

###################################
##                               ##
##             Stops             ##
##                               ##
###################################
stops = SCRAPY_DFS['stops'].copy()
# stops.dropna(how='any', inplace=True)
stops.drop(columns=['item_type'], inplace=True)
stops['stop_id'] = ['{}'.format(i + 1) for i in range(len(stops))]
stops.set_index('stop_id', inplace=True)
stops.to_csv(f'{SCRAPY_OUT_BASE_PATH}stops.txt')

print('STOPS\n', stops)


###################################
##                               ##
##             Trips             ##
##                               ##
###################################

ftm_trips = SCRAPY_DFS['ftm_trains'].copy()
ftm_trips = ftm_trips[ftm_trips['item_type'] == 'Train']
ftm_trips['route_id'] = 'ftm'
ftm_trips.rename(columns={'calendar': 'service_id', 'name': 'trip_id'}, inplace=True)
# ftm_trips['trip_id'] = ['ftm_{}'.format(i + 1) for i in range(len(ftm_trips))]
ftm_trips.drop(columns=['item_type', 'url', 'train_name', 'stop', 'arrival_time', 'departure_time'], inplace=True)
ftm_trips['wheelchair_accessible'] = 1
ftm_trips['trip_id'] = ftm_trips['trip_id'].astype(int).astype(str)
ftm_trips['service_id'] = ftm_trips['service_id'].apply(lambda x: '' if np.isnan(x) else str(int(x)))

print('\n\nFTM TRIPS\n', ftm_trips)

ftm_stop_times = SCRAPY_DFS['ftm_trains'].copy()
ftm_stop_times = ftm_stop_times[ftm_stop_times['item_type'] == 'TripStop']
ftm_stop_times.drop(columns=['item_type', 'url', 'name', 'calendar'], inplace=True)
ftm_stop_times['train_name'] = ftm_stop_times['train_name'].astype(int).astype(str)
ftm_stop_times.rename(columns={'train_name': 'trip_id', 'stop': 'stop_id'}, inplace=True)
stops_tmp = stops.reset_index()
def find_stop_id(stop_name):
  s = stops_tmp[stops_tmp['stop_name'].str.lower() == stop_name.lower()].values
  if len(s) <= 0:
    print(f'Stop {stop_name} not found!')
  return s[0][0] if len(s) > 0 else ''
ftm_stop_times['stop_id'] = ftm_stop_times['stop_id'].apply(find_stop_id)
ftm_stop_times['stop_sequence'] = ftm_stop_times.groupby('trip_id').cumcount() + 1

ftm_trips = add_id_prefix(ftm_trips, 'ftm_', 'trip_id')
ftm_stop_times = add_id_prefix(ftm_stop_times, 'ftm_', 'trip_id')
ftm_stop_times_m = ftm_stop_times.merge(ftm_trips, on='trip_id', how='inner')
print(ftm_stop_times_m)


print('\n\nFTM TRIPS STOPS\n', ftm_stop_times)

def find_train_direction (name):
  tmp = ftm_stop_times_m.loc[ftm_stop_times_m.isnull().any(axis=1)]
  tmp = tmp.loc[ftm_stop_times_m['trip_id'] == name]
  stop = stops_tmp[stops_tmp['stop_id'] == tmp.loc[tmp['arrival_time'].isnull()].drop_duplicates()['stop_id'].values[0]]
  if 'trento' in stop.values[0][1]:
    return '0'
  else:
    return '1'
    
ftm_trips['direction'] = ftm_trips['trip_id'].apply(find_train_direction)
ftm_trips['service_id'] = ftm_trips['service_id'].apply(lambda x: '123450001' if not x else str(x))
ftm_trips.drop_duplicates(inplace=True)
# ftm_trips.set_index('trip_id', inplace=True)





###################################
##                               ##
##             Trips             ##
##                               ##
###################################

trips = SCRAPY_DFS['trento_trains'].copy()
trips = trips[trips['item_type'] == 'Train']
trips.rename(columns={'name': 'trip_id'}, inplace=True)
trips.drop(columns=['item_type', 'url', 'train_name', 'stop', 'arrival_time', 'departure_time'], inplace=True)

trips['service_id'] = '543210001'
trips['wheelchair_accessible'] = 0

print('\n\n\n\n\n\n TRIPS\n', trips)


###################################
##                               ##
##             Routes            ##
##                               ##
###################################

routes = pd.DataFrame([
  ['ftm','1','FTM','Ferrovia Trento Male', 2],
  ['valsugana','1','Valsugana','Ferrovia Valsugana', 2],
  ['vr-bz','2','Verona-Bolzano','Ferrovia Verona-Bolzano', 2],
  ['vr-tn','2','Verona-Trento','Ferrovia Verona-Trento', 2],
  ['rov-bz','2','Rovereto-Bolzano','Ferrovia Rovereto-Bolzano', 2],
  ['tn-ala','2','Trento-Ala','Ferrovia Trento-Ala', 2],
], columns=['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_type'])
routes.set_index('route_id', inplace=True)

stop_times = SCRAPY_DFS['trento_trains'].copy()
stop_times = stop_times[stop_times['item_type'] == 'TripStop']
stop_times.drop(columns=['item_type', 'url', 'name'], inplace=True)
stop_times.rename(columns={'train_name': 'trip_id'}, inplace=True)
stop_times['trip_id'] = stop_times['trip_id'].astype(int).astype(str)
stop_times['stop_id'] = stop_times['stop'].apply(find_stop_id)
stop_times['stop_sequence'] = stop_times.groupby('trip_id').cumcount() + 1
stop_times_m = stop_times.merge(trips, on='trip_id', how='inner')
stop_times.drop(columns=['stop'], inplace=True)

print('\n\n\n\n\n\n STOP TIMES\n', stop_times)



def find_trip_route_and_direction (row):
  name = row['trip_id']
  print(row)
  tmp = stop_times_m.loc[stop_times_m.isnull().any(axis=1)]
  tmp = tmp.loc[stop_times_m['trip_id'] == name]

  route = None
  direction = None

  if len(tmp) <= 0:
    print(f'Missing trip for {name}!')
  else:
    dep, dest = (tmp.iloc[0].values[1].lower(), tmp.iloc[1].values[1].lower())
    print(tmp, '\n', dep, '\n', dest, '\n\n')
    
    vr_bz = ['muenchen', 'napoli', 'roma', 'bologna', 'brennero', 'milano']
    if any(v in dep for v in vr_bz):
      dep = 'bolzano/bozen'
    if any(v in dest for v in vr_bz):
      dest = 'bolzano/bozen'

    vals = ['bassano', 'primolano']
    if any(v in dep for v in vals):
      dep = 'borgo'
    if any(v in dest for v in vals):
      dest = 'borgo'

    if ('verona' in dep and 'bolzano' in dest) or ('verona' in dest and 'bolzano' in dep):
      route = 'vr-bz'
      direction = '1' if 'verona' in dep and 'bolzano' in dest else '0'
    elif ('trento' in dep and 'bolzano' in dest) or ('trento' in dest and 'bolzano' in dep):
      route = 'tn-bz'
      direction = '1' if 'trento' in dep and 'bolzano' in dest else '0'
    elif ('trento' in dep and 'borgo' in dest) or ('trento' in dest and 'borgo' in dep):
      route = 'valsugana'
      direction = '1' if 'trento' in dep and 'borgo' in dest else '0'
    elif ('bolzano' in dep and 'rovereto' in dest) or ('bolzano' in dest and 'rovereto' in dep):
      route = 'rov-bz'
      direction = '1' if 'bolzano' in dep and 'rovereto' in dest else '0'
    elif ('trento' in dep and 'ala' in dest) or ('trento' in dest and 'ala' in dep):
      route = 'tn-ala'
      direction = '1' if 'trento' in dep and 'ala' in dest else '0'
    else:
      pass
      print(dep, '\n', dest, '\n\n')
  
  print(route, direction)
  return pd.Series({'route_id': route, 'direction': direction})

trips[['route_id', 'direction']] = trips.apply(find_trip_route_and_direction, axis=1)
print(len(trips))
trips.dropna(how='any', inplace=True)
print(len(trips))


trips = pd.concat([trips, ftm_trips])
trips['trip_headsign'] = trips['route_id']
trips.to_csv(f'{SCRAPY_OUT_BASE_PATH}trips.txt', index=False)


stop_times = pd.concat([stop_times, ftm_stop_times])
stop_times['arrival_time'] = stop_times['arrival_time'].str.replace('.', ':')
stop_times['departure_time'] = stop_times['departure_time'].str.replace('.', ':')
stop_times.to_csv(f'{SCRAPY_OUT_BASE_PATH}stop_times.txt', index=False)

routes.to_csv(f'{SCRAPY_OUT_BASE_PATH}routes.txt', index=True)