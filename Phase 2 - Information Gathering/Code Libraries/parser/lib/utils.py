import requests
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

from colorama import Fore, init

init(autoreset=True)

def warn (s: str):
  print(f"{Fore.YELLOW}{s}")

def err (s: str):
  print(f"{Fore.RED}{s}")

def info (s: str):
  print(f"{Fore.BLUE}{s}")

def add_id_prefix (df: pd.DataFrame, prefix: str, col='id'):
  df[col] = df[col].map(lambda id: prefix + str(id))
  return df

__OSM_BASE_URL = "https://nominatim.openstreetmap.org/search"

def address_to_lat_lon (address):
  """
    Converts a given address to latitude and longitude coordinates using an external API.

    Parameters:
    - address (str): The address to be converted.

    Returns:
    tuple or None: A tuple containing latitude and longitude coordinates (lat, lon) if the conversion is successful.
                   Returns None if no data is received or an error occurs during the conversion.

    Example:
    >>> result = address_to_lat_lon("1600 Amphitheatre Parkway, Mountain View, CA")
    >>> print(result)
    (37.423021, -122.083739)
    
    Note:
    - The function uses an external API to perform the conversion. Ensure that the provided address is valid.
    - The API response is expected to be in JSON format, and the function extracts the first result's latitude and longitude.
    - If no data is received or an error occurs, the function returns None.
  """
  data = requests.get(__OSM_BASE_URL, params={
    "q": address,
    "format": "json"
  }).json()

  if data:
    first_result = data[0]
    return first_result["lat"], first_result["lon"]
      
  return None


def check_duplicates (df, cols, exits=True):
  """
    Check for duplicate values in the specified columns of a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to check for duplicates.
    - cols (list): A list of column names to check for duplicates.
    - exits (bool): If True, exit the program with an error message if duplicates are found.
                    If False, return False without exiting.

    Returns:
    - bool: True if no duplicates are found, False otherwise (only if exits=False).
  """
  dup = df.loc[df[cols].duplicated()]
  if len(dup) > 0:
    print('ERROR: duplicate cols values!!\n', dup)
    if exits:
      exit(1)
    else:
      return dup
  return True

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in meters
    R = 6371000.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate differences in latitude and longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = R * c

    return distance

def positions_near_enough (p1, p2, THRESHOLD = 500):
  return THRESHOLD > haversine_distance(float(p1['latitude']), float(p1['longitude']), float(p2['latitude']), float(p2['longitude']))