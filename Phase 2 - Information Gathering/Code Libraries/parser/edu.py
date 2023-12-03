import pandas as pd
import numpy as np

from lib.etypes import ETYPE, read_raw_dataset, read_tmp_dataset, exctract_and_fetch_positions, write_tmp_dataset, append_to_tmp_dataset
from lib.utils import add_id_prefix, err, warn, info

edu_fac = read_raw_dataset(ETYPE.EDU_FAC)
edu_fac = edu_fac.iloc[1:5] # FIXME
edu_fac = add_id_prefix(edu_fac, 'edu_fac_')
edu_fac.rename({'name': 'legal_name'}, inplace=True)

# Read tmp positions dataset
positions = read_tmp_dataset(ETYPE.POSITION)
if positions is not None and len(positions) > 0:
  positions = positions.loc[positions['id'].str.contains('edu_')]

# Fetch positions if needed
if positions is None or len(positions) <= 0:
  print('Fetching positions...')
  positions = exctract_and_fetch_positions(edu_fac, 'address', 'edu_')

# Liks edu_fac positions
pos_address_id_map = dict(zip(positions['address'], positions['id']))
edu_fac['localize'] = edu_fac['address'].map(pos_address_id_map)

# Read tmp stops dataset
stops = read_tmp_dataset(ETYPE.STOP)
if stops is not None and len(stops) > 0:
  # TODO find nearest stops
  pass
else:
  edu_fac['nearest_stops'] = None
  err('Could not link nearest stops, please generate stop tmp dataset!')

print('\n\EDU_FAC\n', edu_fac, '\n\nPOSITIONS\n', positions)

write_tmp_dataset(ETYPE.EDU_FAC, edu_fac)
append_to_tmp_dataset(ETYPE.POSITION, positions, False)

