
"""This script scrapes the listings on the Hemnet Slutpris section for Stockholm and outputs a csv with a table with the following variables:
adress, stadsdel, maklare, storlek, rum, avgift, datum, slutpris, pris_per_meter, percent_over, utgangs_pris"""

import pandas as pd
import requests
import bs4 as bs
import pandas as pd
import re as re

url = 'https://www.hemnet.se/salda/bostader?location_ids%5B%5D=473379&sold_age=6m'
response = requests.get(url)
code = response.text
parsed = bs.BeautifulSoup(code, "html.parser")
listings = parsed.findAll('div',{'class':'sold-property-listing'})

#Find address
def get_address(listings):
    addresser = []
    for entry in listings:
    locations = entry.findAll('div', {'class':'sold-property-listing__location'})
    for entry in locations:
        str_entry = str(entry)
        id_location = str_entry.find('item-link')
        if id_location>=0:
            start_location = id_location + 11
            remaining = str_entry[start_location:]
            end_location = remaining.find('<')
            remaining = remaining[:end_location]
        else:
            remaining = 'Saknas'
        addresser.append(remaining)
        return addresser

#Find neighborhood
def get_stadsdel(listings):
    stadsdelar = []
    for entry in listings:
    locations = entry.findAll('div', {'class':'sold-property-listing__location'})
    for entry in locations:
        str_entry = str(entry)
        id_location = str_entry.find('<span class="item-link"') + 1
        if id_location>0:
            start_location = id_location + 25
            remaining = str_entry[start_location:]
            remaining = remaining.lstrip(' ')
            end_location = str(remaining).find(',')
            remaining = remaining[:end_location]
        else:
            remaining = 'Saknas'
        stadsdelar.append(remaining)
        return stadsdelar

#Find final price
def get_slutpris(listings):
    prices_extracted = []
    #Extract section of HTML that contains price information
    for entry in listings:
        subentry = entry.findAll('div',{'class':'sold-property-listing__price'})
        for sub in subentry:
            sub2 = sub.findAll('div', {'class': 'clear-children'})
            for sub3 in sub2:
                price = sub3.findAll('span', {'class': 'sold-property-listing__subheading sold-property-listing--left'})
                if len(price)>0:
                    prices_extracted.append(price)
    #Remove evertying in this part before Slutpris
    prices_to_clean = []
    for price in prices_extracted:
        location = str(price).find('Slut')
        price_short = str(price)[location:]
        prices_to_clean.append(price_short)
    #First remove //xa0 tags and then extract only the numbers in the remaining string
    clean_prices = []
    for price in prices_to_clean:
        remove_loc = price.find('\\xa0')
        while remove_loc>=0:
            price = price[:remove_loc] + price[remove_loc+4:]
            remove_loc = price.find('\\xa0')
        price = filter(str.isdigit, price)
        clean_prices.append(price)
    return clean_prices
    
    