import pandas as pd
import os

from enum import Enum
from lib.utils import address_to_lat_lon, err, warn, info, add_id_prefix

################################
##                            ##
##         Constants          ##
##                            ##
################################

__RAW_BASE_PATH = '../../Raw data/'
__TMP_DF_DIR = 'tmp_df/'

class ETYPE(Enum):
  USER = {
    'name': 'user',
    'filename': 'users/users',
    'columns': ['name', 'occupation', 'special_needs'],
    'relations': ['domiciled', 'reside', 'work']
  }
  EDU_FAC = {
    'name': 'educational_facility',
    'filename': 'edu/educational_facilities',
    'columns': ['type', 'name'],
    'relations': ['nearest_stops']
  }
  POSITION = {
    'name': 'position',
    'filename': 'positions',
    'columns': ['address', 'latitude', 'longitude'],
    'relations': []
  }



################################
##                            ##
##    Read/Write functions    ##
##                            ##
################################

def __get_raw_file_path (etype: ETYPE):
  return f'{__RAW_BASE_PATH}{etype.value["filename"]}.csv'

def __get_tmp_file_path (etype: ETYPE):
  return f'{__TMP_DF_DIR}{etype.value["filename"]}.csv'

def read_raw_dataset (etype: ETYPE):
  try:
    return pd.read_csv(__get_raw_file_path(etype))
  except FileNotFoundError:
    info(f"Raw file '{os.path.abspath(__get_raw_file_path(etype))}' not found.")

def read_tmp_dataset (etype: ETYPE):
  try:
    return pd.read_csv(__get_tmp_file_path(etype))
  except FileNotFoundError:
    info(f"Raw file '{os.path.abspath(__get_tmp_file_path(etype))}' not found.")

def clean_columns (etype: ETYPE, df: pd.DataFrame):
  to_keep = etype.value['columns'] + etype.value['relations'] + ['id']
  cols = df.columns.to_list()
  for c in to_keep:
    if c not in cols:
      err(f'Missing required column "{c}" for etype "{etype}"')
      exit(1)
  return df.drop(columns=[c for c in cols if c not in to_keep])

def fix_id_col (df: pd.DataFrame):
  print(df, df.columns.to_list())
  if 'id' not in df.columns.to_list():
    df = df.reset_index()
    if 'id' not in df.columns.to_list() and 'index' in df.columns.to_list():
      df = df.rename(columns={'index': 'id'})
    df['id'] = df['id'].astype(str)
    print(df, df.columns.to_list())
  return df

def write_tmp_dataset (etype: ETYPE, df: pd.DataFrame):
  df = fix_id_col(df)
  df = clean_columns(etype, df)

  path = __get_tmp_file_path(etype)
  os.makedirs(os.path.dirname(path), exist_ok=True)

  df.to_csv(path, index=False)

def append_to_tmp_dataset (etype: ETYPE, df: pd.DataFrame, skip_if_exists=True):
  df = fix_id_col(df)
  df = clean_columns(etype, df)

  curr_df = read_tmp_dataset(etype)
  if curr_df is not None and len(df) > 0:
    if skip_if_exists:
      return
    df = pd.concat([curr_df, df])

  path = __get_tmp_file_path(etype)
  os.makedirs(os.path.dirname(path), exist_ok=True)

  df.to_csv(path, index=False)



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