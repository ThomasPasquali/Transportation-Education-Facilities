import pandas as pd
import numpy as np

from lib.etypes import ETYPE, read_raw_dataset, read_tmp_dataset, exctract_and_fetch_positions, write_tmp_dataset, append_to_tmp_dataset

edu_fac = read_raw_dataset(ETYPE.EDU_FAC)
edu_fac.set_index('id', inplace=True)

# Read tmp positions dataset
positions = read_tmp_dataset(ETYPE.POSITION)
if positions is not None and len(positions) > 0:
  positions = positions.loc[positions['id'].str.contains('edu_')]

# Fetch positions if needed
if positions is None or len(positions) <= 0:
  print('Fetching positions...')
  positions = exctract_and_fetch_positions(edu_fac, 'address', 'edu_')

# print(positions)
# pos_address_id_map = dict(zip(positions['address'], positions['id']))
# edu_fac['localize'] = edu_fac['address'].map(pos_address_id_map)

# Clean columns
edu_fac.drop(columns=['address'], inplace=True)
edu_fac.rename({'name': 'legal_name'})

positions.set_index('id', inplace=True)

print('\n\EDU_FAC\n', edu_fac, '\n\nPOSITIONS\n', positions)

append_to_tmp_dataset(ETYPE.EDU_FAC, edu_fac)
append_to_tmp_dataset(ETYPE.POSITION, positions)

