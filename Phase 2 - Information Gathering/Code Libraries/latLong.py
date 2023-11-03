import requests

address = "Via Perlasca 4, Mezzolomabrdo, 38017, TN"

base_url = "https://nominatim.openstreetmap.org/search"
params = {
    "q": address,
    "format": "json"
}

response = requests.get(base_url, params=params)
data = response.json()

if data:
    first_result = data[0]
    latitude = first_result["lat"]
    longitude = first_result["lon"]
    print("Latitudine:", latitude)
    print("Longitudine:", longitude)
else:
    print("Geocodifica non riuscita")