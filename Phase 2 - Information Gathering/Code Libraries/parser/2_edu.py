import pandas as pd
import numpy as np

from lib.etypes import ETYPE, read_raw_dataset, read_tmp_dataset, exctract_and_fetch_positions, write_tmp_dataset, append_to_tmp_dataset
from lib.utils import add_id_prefix, err, warn, info, positions_near_enough

edu_fac = read_raw_dataset(ETYPE.EDU_FAC)
edu_fac = add_id_prefix(edu_fac, 'edu_fac_')
edu_fac.rename({'name': 'legal_name'}, inplace=True)

# Read tmp positions dataset
positions = read_tmp_dataset(ETYPE.POSITION)
if positions is not None and len(positions) > 0:
  edu_positions = positions.loc[positions['id'].str.contains('pos_edu_fac_')]

# Fetch positions if needed
if edu_positions is None or len(edu_positions) < len(edu_fac):
  print('Fetching positions...')
  edu_positions = exctract_and_fetch_positions(edu_fac, 'address', 'pos_edu_fac_')

# Liks edu_fac positions
pos_address_id_map = dict(zip(edu_positions['address'], edu_positions['id']))
edu_fac['localize'] = edu_fac['address'].map(pos_address_id_map)

# Read tmp stops dataset
# stops = read_tmp_dataset(ETYPE.STOP)
stops_position = positions.loc[positions['id'].str.contains('pos_stop')] 
if stops_position is not None and len(stops_position) > 0:
  edu_positions.set_index('id', inplace=True)

  def find_nearest_stops (edu):
    e_pos = edu_positions.loc[pos_address_id_map[edu['address']]]
    near_stops = stops_position[stops_position.apply(lambda s: positions_near_enough(e_pos, s), axis=1)]
    return '|'.join(near_stops['id'])
  edu_fac['nearest_stops'] = edu_fac.apply(find_nearest_stops, axis=1)

  edu_positions.reset_index(inplace=True)
  pass
else:
  edu_fac['nearest_stops'] = None
  err('Could not link nearest stops, please generate stop tmp dataset!')

print('\n\nEDU_FAC\n', edu_fac, '\n\nPOSITIONS\n', edu_positions)

write_tmp_dataset(ETYPE.EDU_FAC, edu_fac)
append_to_tmp_dataset(ETYPE.POSITION, edu_positions, False)

