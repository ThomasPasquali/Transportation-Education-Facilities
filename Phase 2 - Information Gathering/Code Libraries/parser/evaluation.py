import pandas as pd
import numpy as np

from lib.etypes import ETYPE, read_raw_dataset, read_tmp_dataset, exctract_and_fetch_positions, write_tmp_dataset, append_to_tmp_dataset
from lib.utils import add_id_prefix, err, warn, info, positions_near_enough

DFS = {}
etypes = [e.value for e in ETYPE]
conn_matrix = pd.DataFrame(columns=[e['name'] for e in etypes], index=[e['name'] for e in etypes])
legend = pd.DataFrame(columns=['Etype - Etype', 'Property names'])

for e in ETYPE:
  DFS[e.value['name']] = read_tmp_dataset(e)

for etype1 in ETYPE:
  etype1_v = etype1.value
  etype1_name = etype1_v['name']
  df = DFS[etype1_name]

  for etype2 in ETYPE:
    etype2_v = etype2.value
    etype2_name = etype2_v['name']

    res = []
    tot = np.NAN
    columns = []

    if etype1 == etype2:
      columns = etype1_v['columns']      
    else:
      for i in range(len(etype1_v['relations'])):
        if etype2_name == etype1_v['relations_etype'][i]:
          columns.append(etype1_v['relations'][i])

    tot = np.NAN
    if len(columns) > 0:
      tot = 0
      for c in columns:
        res.append(df[c].isnull().sum() / len(df[c]))
        tot += df[c].isnull().sum()
      tot /= len(columns) * len(df)

    # if tot > 1:
    #   print(f'{etype1_name} - {etype2_name} {columns}  {tot}')

    legend.loc[len(legend)] = [f'{etype1_name} - {etype2_name}', ' | '.join(columns)]
    conn_matrix[etype2_name][etype1_name] = ' | '.join(['{:.2f}'.format(v) for v in res]) + ' tot: ' + '{:.2f}'.format(tot) if not np.isnan(tot) else ''
  
# print(conn_matrix)
conn_matrix.to_csv('../../../Phase 5 - Data Definition/connectivity_matrix.csv', index=True)
legend.to_csv('../../../Phase 5 - Data Definition/connectivity_matrix_legend.csv', index=False)