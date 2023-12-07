import pandas as pd
import numpy as np

from lib.etypes import ETYPE, read_raw_dataset, append_to_tmp_dataset, exctract_and_fetch_positions, read_tmp_dataset, write_tmp_dataset
from lib.utils import check_duplicates, err, warn, info, add_id_prefix

users = read_raw_dataset(ETYPE.USER)
users = add_id_prefix(users, 'u_')

# Read tmp positions dataset
positions = read_tmp_dataset(ETYPE.POSITION)
if positions is not None:
  user_positions = positions.loc[positions['id'].astype(str).str.contains('u_dom_|u_res_')]

# Fetch positions if needed
if user_positions is None or len(user_positions) <= len(users):
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
edu_pos = read_tmp_dataset(ETYPE.POSITION) 
if edu_pos is not None and len(edu_pos) > 0:
  edu_address_id_map = dict(zip(edu_pos['address'], edu_pos['id']))
  users['work'] = users['work_location'].map(edu_address_id_map)
else:
  users['work'] = None
  err('Could not link work locations, please generate educational facilities tmp dataset!')

# Schedules
shifts = read_raw_dataset(ETYPE.SHIFT)
schedules = read_raw_dataset(ETYPE.WEEKLY_SCHEDULE, custom_path='users/calendar')
schedules_exceptions = read_raw_dataset(ETYPE.SCHEDULE_EXCEPTION, custom_path='users/calendar_dates')


print(
  '\n\nUSERS\n', users,
  '\n\nPOSITIONS\n', positions,
  '\n\nWEEKLY SCHEDULE\n', schedules,
  '\n\nSCHEDULE EXCEPTION\n', schedules_exceptions,
  '\n\SHIFTS\n', shifts
  )

write_tmp_dataset(ETYPE.USER, users)
write_tmp_dataset(ETYPE.SHIFT, shifts)
append_to_tmp_dataset(ETYPE.POSITION, positions, False)
append_to_tmp_dataset(ETYPE.WEEKLY_SCHEDULE, schedules, False)
append_to_tmp_dataset(ETYPE.SCHEDULE_EXCEPTION, schedules_exceptions, False)


