import requests
import pandas as pd

#define variables, could add others for maxPrice etc
boroughs = {
    "Lambeth": "5E93971",
    "Southwark": "5E61518",
    }

pages = 5

# define our user headers
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}

output = []
for name,borough_code in boroughs.items():
    for page in range(1,pages+1):
        min = 50000
        max = 1000000
        url = f"https://www.rightmove.co.uk/api/_search?locationIdentifier=REGION%{borough_code}&numberOfPropertiesPerPage=24&radius=0.0&sortType=2&index={str(24*page)}&maxBedrooms=3&minBedrooms=2&maxPrice={max}&minPrice={min}&sortType=6&propertyTypes=&includeSSTC=false&viewType=LIST&channel=BUY&areaSizeUnit=sqft&currencyCode=GBP&isFetching=false"
        print(f'Scraping: {name} - Page: {page}')
        data = requests.get(url,headers=headers).json()
        properties = data['properties']
        output.extend(properties)

df = pd.json_normalize(output)

df.to_csv('allcolumns.csv',index=False)