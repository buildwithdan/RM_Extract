import requests
import pandas as pd

#define variables, could add others for maxPrice etc
boroughs = {
    "City of London": "5E61224",
    "Barking and Dagenham": "5E61400",
    "Barnet": "5E93929",
    "Bexley": "5E93932",
    "Brent": "5E93935",
    "Bromley": "5E93938",
    "Camden": "5E93941",
    "Croydon": "5E93944",
    "Ealing": "5E93947",
    "Enfield": "5E93950",
    "Greenwich": "5E61226",
    "Hackney": "5E93953",
    "Hammersmith and Fulham": "5E61407",
    "Haringey": "5E61227",
    "Harrow": "5E93956",
    "Havering": "5E61228",
    "Hillingdon": "5E93959",
    "Hounslow": "5E93962",
    "Islington": "5E93965",
    "Kensington and Chelsea": "5E61229",
    "Kingston upon Thames": "5E93968",
    "Lambeth": "5E93971",
    "Lewisham": "5E61413",
    "Merton": "5E61414",
    "Newham": "5E61231",
    "Redbridge": "5E61537",
    "Richmond upon Thames": "5E61415",
    "Southwark": "5E61518",
    "Sutton": "5E93974",
    "Tower Hamlets": "5E61417",
    "Waltham Forest": "5E61232",
    "Wandsworth": "5E93977",
    "Westminster": "5E93980",
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

df.to_csv('z.allcolumns4.csv',index=False)
print('Completed')