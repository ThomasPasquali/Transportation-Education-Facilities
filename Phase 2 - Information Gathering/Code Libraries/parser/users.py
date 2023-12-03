import pandas as pd
import numpy as np

from lib.etypes import ETYPE, read_raw_dataset, append_to_tmp_dataset, exctract_and_fetch_positions, read_tmp_dataset, write_tmp_dataset
from lib.utils import check_duplicates, err, warn, info, add_id_prefix

users = read_raw_dataset(ETYPE.USER)
users = add_id_prefix(users, 'u_')

# Read tmp positions dataset
positions = read_tmp_dataset(ETYPE.POSITION)
if positions is not None:
  positions = positions.loc[positions['id'].astype(str).str.contains('u_dom_|u_res_')]

# Fetch positions if needed
if positions is None or len(positions) <= 0:
  print('Fetching positions...') 
  positions = pd.concat([
    exctract_and_fetch_positions(users, 'domicile_location', 'u_dom_'),
    exctract_and_fetch_positions(users, 'residence_location', 'u_res_'),
  ])

# Remove duplicates (TODO change duplciates id prefix?)
positions.drop_duplicates(subset='address', inplace=True)
check_duplicates(positions, ['address'])

# Link positions to users
pos_address_id_map = dict(zip(positions['address'], positions['id']))
users['domiciled'] = users['domicile_location'].map(pos_address_id_map)
users['reside'] = users['residence_location'].map(pos_address_id_map)

# Read tmp edu dataset
edu = read_tmp_dataset(ETYPE.EDU_FAC)
if edu is not None and len(edu) > 0:
  edu_address_id_map = dict(zip(edu['address'], edu['id']))
  users['work'] = users['work_location'].map(edu_address_id_map)
else:
  users['work'] = None
  err('Could not link work locations, please generate educational facilities tmp dataset!')

print('\n\nUSERS\n', users, '\n\nPOSITIONS\n', positions)

write_tmp_dataset(ETYPE.USER, users)
append_to_tmp_dataset(ETYPE.POSITION, positions, False)

