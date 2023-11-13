import bs4, requests
import pandas as pd
import re 

typeEdu = 'university'
url = 'https://webapps.unitn.it/du/it/StrutturaAccademica' 
file_path = '../../Raw data/edu/university.csv'

response = requests.get(url) 
response.raise_for_status()
soup = bs4.BeautifulSoup(response.text, 'html.parser') 

school_infos = []

div = soup.find('div', class_='struttura-accademica')
departements = div.find_all('div', class_=re.compile(r'struttura dip-'))

for department in departements:
    name = department.find('h2').text.strip() 
    address = department.find('div', class_='indirizzo').text
    
    school_info = [typeEdu, name, address] 
    school_infos.append(school_info)

df_university = pd.DataFrame(school_infos, columns=['type', 'name', 'address'])
df_university = df_university.drop_duplicates(subset=['name', 'address'])  
df_university['name'] = df_university['name'].str.replace(',', ';')
df_university['address'] = df_university['address'].str.replace(',', '')
df_university.insert(0, 'id', range(1, len(df_university) + 1))
pd.set_option('display.max_colwidth', None)
df_university.to_csv(file_path, index=False)
#print(df_university)  
