import requests
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

#define variables, could add others for maxPrice etc
boroughs = {
    "City of London": "5E61224",
    "Barking and Dagenham": "5E61400",
     }

#pages = 5

# define our user headers
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}

output = []

print('Starting')

for name,borough_code in boroughs.items():
  min = 50000
  max = 1000000
  url = f"https://www.rightmove.co.uk/api/_search?locationIdentifier=REGION%{borough_code}&numberOfPropertiesPerPage=24&radius=0.0&sortType=2&maxBedrooms=3&minBedrooms=2&maxPrice={max}&minPrice={min}&sortType=6&propertyTypes=&includeSSTC=false&viewType=LIST&channel=BUY&areaSizeUnit=sqft&currencyCode=GBP&isFetching=false"
  data = requests.get(url,headers=headers).json()
  properties = data['properties']
  output.extend(properties)
  print(f"{name} Completed")

df = pd.json_normalize(output)

print('Completed')

engine = create_engine('postgresql://dnellpersonal:v2_3v2ej_AZxVQBp87rqyu86nFyUwqiX@db.bit.io/dnellpersonal/rightmove_large')

#df.to_csv('z.allcolumns4.csv',index=False)

df.to_sql('data', engine)

Print('Inserted in DB')