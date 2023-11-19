import pandas as pd

dlr = pd.read_csv('./DomainLanguageResources_custom.csv')

df = pd.DataFrame(columns=['concept labels', 'description'])
df['concept labels'] = dlr['Concepts'] + '_' + dlr['ID']
df['description'] = dlr['Description']

for r in dlr.iterrows():
  r = r[1]
  print(f"{r.values[0]} & {r.values[1]} & {r.values[2]} & {r.values[3]}\\\\")

# print(df)
df.to_csv('./DomainLanguageResources.csv', index=False)
