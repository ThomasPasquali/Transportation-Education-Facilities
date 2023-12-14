import pandas as pd
import os

from enum import Enum
from lib.utils import address_to_lat_lon, err, warn, info, add_id_prefix

################################
##                            ##
##         Constants          ##
##                            ##
################################

RAW_BASE_PATH = '../../Raw data/'
__TMP_DF_DIR = 'tmp_df/'

class ETYPE(Enum):
  # Transportation
  PROVIDER = {
    'name': 'provider',
    'filename': 'transport/providers',
    'columns': ['name'],
    'relations': [],
    'relations_etype': []
  }
  STOP = {
    'name': 'stop',
    'filename': 'transport/stops',
    'columns': ['name', 'type'],
    'relations': ['localize'],
    'relations_etype': ['position']
  }
  ROUTE = {
    'name': 'route',
    'filename': 'transport/routes',
    'columns': ['long_name', 'short_name', 'type'],
    'relations': ['operated'],
    'relations_etype': ['provider']
  }
  JOURNEY = {
    'name': 'journey',
    'filename': 'transport/journeys',
    'columns': ['headsign', 'direction', 'accessibility'],
    'relations': ['characterized', 'avaiability_schedule', 'avaiability_schedule_exception'],
    'relations_etype': ['route', 'weekly_schedule', 'schedule_exception']
  }
  JOURNEY_STOP = {
    'name': 'journey_stop',
    'filename': 'transport/journeys_stops',
    'columns': ['arrival_time', 'departure_time', 'stop_sequence'],
    'relations': ['of', 'at'],
    'relations_etype': ['journey', 'stop']
  }

  # End users
  USER = {
    'name': 'user',
    'filename': 'users/users',
    'columns': ['name', 'occupation', 'special_needs'],
    'relations': ['domiciled', 'reside', 'work'],
    'relations_etype': ['position', 'position', 'position']
  }
  SHIFT = {
    'name': 'shift',
    'filename': 'users/shifts',
    'columns': ['arrive_before', 'leave_after'],
    'relations': ['from', 'to', 'occurence_schedule', 'occurence_schedule_exception', 'involvement'],
    'relations_etype': ['position', 'position', 'weekly_schedule', 'schedule_exception', 'user']
  }

  # Education
  EDU_FAC = {
    'name': 'educational_facility',
    'filename': 'edu/educational_facilities',
    'columns': ['type', 'legal_name'],
    'relations': ['localize'], # 'nearest_stops'
    'relations_etype': ['position']
  }

  # Common
  POSITION = {
    'name': 'position',
    'filename': 'positions',
    'columns': ['address', 'latitude', 'longitude'],
    'relations': []
  }
  WEEKLY_SCHEDULE = {
    'name': 'weekly_schedule',
    'filename': 'calendar',
    'columns': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date'],
    'relations': []
  }
  SCHEDULE_EXCEPTION = {
    'name': 'schedule_exception',
    'filename': 'calendar_dates',
    'columns': ['date', 'type'],
    'relations': []
  }

def get_complete_columns_list(etype: ETYPE):
  return ['id'] + etype.value['columns'] + etype.value['relations']



################################
##                            ##
##    Read/Write functions    ##
##                            ##
################################

def __get_raw_file_path (etype: ETYPE, file_extention='.csv', custom_path=None):
  return f'{RAW_BASE_PATH}{custom_path if custom_path is not None else etype.value["filename"]}{file_extention}'

def __get_tmp_file_path (etype: ETYPE, file_extention='.csv'):
  return f'{__TMP_DF_DIR}{etype.value["filename"]}{file_extention}'

def read_raw_dataset (etype: ETYPE, file_extention='.csv', custom_path=None):
  try:
    return pd.read_csv(__get_raw_file_path(etype, file_extention, custom_path))
  except FileNotFoundError:
    info(f"Raw file '{os.path.abspath(__get_raw_file_path(etype))}' not found.")

def read_tmp_dataset (etype: ETYPE):
  try:
    return pd.read_csv(__get_tmp_file_path(etype))
  except FileNotFoundError:
    info(f"Raw file '{os.path.abspath(__get_tmp_file_path(etype))}' not found.")

def clean_columns (etype: ETYPE, df: pd.DataFrame):
  to_keep = get_complete_columns_list(etype)
  cols = df.columns.to_list()
  for c in to_keep:
    if c not in cols:
      err(f'Missing required column "{c}" for etype "{etype}"')
      exit(1)
  df = df.drop(columns=[c for c in cols if c not in to_keep])
  cols = df.columns.to_list()
  cols.remove('id')
  df = df[['id'] + cols]
  return df

def fix_id_col (df: pd.DataFrame):
  if 'id' not in df.columns.to_list():
    df = df.reset_index()
    if 'id' not in df.columns.to_list() and 'index' in df.columns.to_list():
      df = df.rename(columns={'index': 'id'})
    df['id'] = df['id'].astype(str)
  return df

def write_tmp_dataset (etype: ETYPE, df: pd.DataFrame, file_extention='.csv'):
  df = fix_id_col(df)
  df = clean_columns(etype, df)

  path = __get_tmp_file_path(etype,file_extention=file_extention)
  os.makedirs(os.path.dirname(path), exist_ok=True)

  df.to_csv(path, index=False)
  return df

def append_to_tmp_dataset (etype: ETYPE, df: pd.DataFrame, skip_if_exists=True):
  df = fix_id_col(df)
  df = clean_columns(etype, df)

  curr_df = read_tmp_dataset(etype)
  if curr_df is not None and len(df) > 0:
    if skip_if_exists:
      return
    df = pd.concat([curr_df, df])
    df = df.drop_duplicates(subset='id', keep='first')

  path = __get_tmp_file_path(etype)
  os.makedirs(os.path.dirname(path), exist_ok=True)

  df.to_csv(path, index=False)
  return df



################################
##                            ##
##     DataFrames parsers     ##
##                            ##
################################

def exctract_and_fetch_positions(df: pd.DataFrame, col: str, id_prefix: str):
  info = []
  for i, row in df.iterrows():
    info.append({'id': i, 'address': row[col]})

  positions = pd.DataFrame(info, columns=['id', 'address'])
  positions.drop_duplicates(subset='address', inplace=True)
  positions = add_id_prefix(positions, id_prefix)
  positions[['latitude', 'longitude']] = positions['address'].apply(address_to_lat_lon).apply(pd.Series)

  return positions