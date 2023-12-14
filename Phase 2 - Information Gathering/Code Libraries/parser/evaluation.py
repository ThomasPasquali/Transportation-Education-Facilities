import pandas as pd
import numpy as np

from lib.etypes import ETYPE, read_raw_dataset, read_tmp_dataset, exctract_and_fetch_positions, write_tmp_dataset, append_to_tmp_dataset
from lib.utils import add_id_prefix, err, warn, info, positions_near_enough

DFS = {}
etypes = [e.value for e in ETYPE]
conn_matrix = pd.DataFrame(columns=[e['name'] for e in etypes], index=[e['name'] for e in etypes])

for e in ETYPE:
  DFS[e.value['name']] = read_tmp_dataset(e)

for etype1 in ETYPE:
  etype1_v = etype1.value
  etype1_name = etype1_v['name']
  df = DFS[etype1_name]

  for etype2 in ETYPE:
    etype2_v = etype2.value
    etype2_name = etype2_v['name']

    value = np.NAN
    if etype1 == etype2:
      value = df[etype1_v['columns']].isnull().sum().sum() / df[etype1_v['columns']].count().sum()
    else:
      columns = []
      for i in range(len(etype1_v['relations'])):
        if etype2_name == etype1_v['relations_etype'][i]:
          columns.append(etype1_v['relations'][i])
      print(etype1_name, etype2_name, columns)
      if len(columns) > 0:
        value = df[columns].isnull().sum().sum() / df[columns].count().sum()

    conn_matrix[etype1_name][etype2_name] = value
  
print(conn_matrix)
conn_matrix.to_csv('../../../Phase 5 - Data Definition/connectivity_matrix.csv')