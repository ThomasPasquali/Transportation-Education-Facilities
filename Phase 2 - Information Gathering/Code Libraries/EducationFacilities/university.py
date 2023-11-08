import bs4, requests
import pandas as pd
import re 

typeEdu = 'university'
url = 'https://webapps.unitn.it/du/it/StrutturaAccademica' 
file_path = r'C:\Users\Riccardo\OneDrive\Magistrale\Semestre1\KnowledgeGraphEngineering\EducationFacilities\university.csv'

response = requests.get(url) 
response.raise_for_status()
soup = bs4.BeautifulSoup(response.text, 'html.parser') 

school_infos = []

div = soup.find('div', class_='struttura-accademica')
departements = div.find_all('div', class_=re.compile(r'struttura dip-'))

for department in departements:
    name = department.find('h2').text.strip() 
    address = department.find('div', class_='indirizzo').text

    nominatim = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json"
    }

    response1 = requests.get(nominatim, params=params)
    data = response1.json()

    if data:
        first_result = data[0]
        latitude = first_result["lat"]
        longitude = first_result["lon"]
    else:
        latitude = '-'
        longitude = '-'
        
    school_info = [typeEdu, name, address, latitude, longitude]
    school_infos.append(school_info)

df_university = pd.DataFrame(school_infos, columns=['typeEdu', 'name', 'address','latitude', 'longitude'])
df_university = df_university.drop_duplicates(subset=['name', 'address'])  
pd.set_option('display.max_colwidth', None)
df_university.to_csv(file_path, index=False)
#print(df_university)  
