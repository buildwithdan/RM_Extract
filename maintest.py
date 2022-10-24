# importing our libraries

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random

"""
Rightmove uses specific codes to describe each London borough, I have 
manually collected these codes by search for each borough individually.
"""

BOROUGHS = {
    "City of London": "5E61224",
    "Barking and Dagenham": "5E61400",

}


def main():

    # initialise index, this tracks the page number we are on. every additional page adds 24 to the index

    # create lists to store our data
    all_apartment_links = []
    all_description = []
    all_address = []
    all_price = []
    output = []

    # apparently the maximum page limit for rightmove is 42
    for borough in list(BOROUGHS.values()):

        # initialise index, this tracks the page number we are on. every additional page adds 24 to the index
        index = 0

        key = [key for key, value in BOROUGHS.items() if value == borough]
        print(f"We are scraping the borough named: {key}")
        for pages in range(41):

            # define our user headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            }

            url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
          
            # the website changes if the you are on page 1 as compared to other pages
            if index == 0:
                rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

            elif index != 0:
                rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&index={index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

            # request our webpage
            res = requests.get(rightmove, headers=headers)

            # check status
            res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")

            # This gets the list of apartments
            apartments = soup.find_all("div", class_="l-searchResult is-list")

            # This gets the number of listings
            number_of_listings = soup.find(
                "span", {"class": "searchHeader-resultCount"}
            )
            number_of_listings = number_of_listings.get_text()
            number_of_listings = int(number_of_listings.replace(",", ""))

            data = requests.get(url,headers=headers).json()
            properties = data['properties']
            output.extend(properties)
          
            for i in range(len(apartments)):

                # tracks which apartment we are on in the page
                apartment_no = apartments[i]
   
                          
                # append link
                apartment_info = apartment_no.find("a", class_="propertyCard-link")
                link = "https://www.rightmove.co.uk" + apartment_info.attrs["href"]
                all_apartment_links.append(link)

                # append address
                address = (
                    apartment_info.find("address", class_="propertyCard-address")
                    .get_text()
                    .strip()
                )
                all_address.append(address)

                # append description
                description = (
                    apartment_info.find("h2", class_="propertyCard-title")
                    .get_text()
                    .strip()
                )
                all_description.append(description)

                # append price
                price = (
                    apartment_no.find("div", class_="propertyCard-priceValue")
                    .get_text()
                    .strip()
                )
                all_price.append(price)

          
            print(f"You have scrapped {pages + 1} pages of apartment listings.")
            print(f"You have {number_of_listings - index} listings left to go")
            print("\n")

            # code to ensure that we do not overwhelm the website
            time.sleep(random.randint(1, 3))

            # Code to count how many listings we have scrapped already.
            index = index + 24

            if index >= number_of_listings:
                break

              

    # convert data to dataframe
   
    data = {
        "Links": all_apartment_links,
        "Address": all_address,
        "Description": all_description,
        "Price": all_price,
    }
    
  
    #df = pd.DataFrame.from_dict(data)
    #df.to_csv(r"sales_data.csv", encoding="utf-8", header="true", index = False)

    df = pd.json_normalize(output)
    df.to_csv('scraped_data.csv',index=False)


if __name__ == "__main__":
    main()