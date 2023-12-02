import pandas as pd
import os

from enum import Enum
from lib.utils import address_to_lat_lon


################################
##                            ##
##         Constants          ##
##                            ##
################################

__RAW_BASE_PATH = '../../Raw data/'
__TMP_DF_DIR = 'tmp_df/'

class ETYPE(Enum):
  USER = 'users/users'
  EDU_FAC = 'edu/educational_facilities'
  POSITION = 'position'



################################
##                            ##
##    Read/Write functions    ##
##                            ##
################################

def __get_raw_file_path (etype: ETYPE):
  return f'{__RAW_BASE_PATH}{etype.value}.csv'

def __get_tmp_file_path (etype: ETYPE):
  return f'{__TMP_DF_DIR}{etype.value}.csv'

def read_raw_dataset (etype: ETYPE):
  try:
    return pd.read_csv(__get_raw_file_path(etype))
  except FileNotFoundError:
    print(f"Raw file '{os.path.abspath(__get_raw_file_path(etype))}' not found.")

def read_tmp_dataset (etype: ETYPE):
  try:
    return pd.read_csv(__get_tmp_file_path(etype))
  except FileNotFoundError:
    print(f"Raw file '{os.path.abspath(__get_tmp_file_path(etype))}' not found.")

def write_tmp_dataset (etype: ETYPE, df: pd.DataFrame):
  path = __get_tmp_file_path(etype)
  os.makedirs(os.path.dirname(path), exist_ok=True)
  df.to_csv(path)

def append_to_tmp_dataset (etype: ETYPE, df: pd.DataFrame):
  curr_df = read_tmp_dataset(etype)
  if curr_df is not None and len(df) > 0:
    df = pd.concat([curr_df, df])
  path = __get_tmp_file_path(etype)
  os.makedirs(os.path.dirname(path), exist_ok=True)
  df.to_csv(path)



################################
##                            ##
##     DataFrames parsers     ##
##                            ##
################################

def exctract_positions(df: pd.DataFrame, col: str, id_prefix: str):
  info = []
  for i, row in df.iterrows():
    info.append({'id': i, 'address': row[col]})

  positions = pd.DataFrame(info, columns=['id', 'address'])
  positions.drop_duplicates(subset='address', inplace=True)
  positions['id'] = positions['id'].map(lambda id: id_prefix + str(id) )
  positions[['latitude', 'longitude']] = positions['address'].apply(address_to_lat_lon).apply(pd.Series)

  return positions