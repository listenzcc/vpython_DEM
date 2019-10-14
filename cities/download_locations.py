# -*- coding: utf-8 -*-
# Download data from http://bjtime.cn/shicha
# Locations of cities in china
# locations is saved as json file in locations.json

import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup

# The site seems protective,
# if you spide data once, it will block you for a long time.
# so be careful.
url = 'http://bjtime.cn/shicha/'


# fetch html_doc from url and return BeautifulSoup object
def fetch_html(url, coding='utf-8', features='html5lib'):
    # Request response from url
    res = requests.get(url)
    # Change coding
    res.encoding = coding
    # Return BeautifulSoup using specified features
    return BeautifulSoup(res.text, features=features)


# locations will be stored here
locations = dict()

# Start parsing
# for each province/state
for state in fetch_html(url).find_all('a', style="TEXT-DECORATION: none"):
    # state name
    print(state.text)
    locations[state.text] = dict()

    # for each city in the state, read its N/E position
    for city in fetch_html(url+state.get('href')).find_all('tr')[1:]:
        contents = [x.text for x in city.find_all('td')[:3]]
        locations[state.text][contents[0]] = contents[1:]

# locations should be filled
pprint(locations)

# Solid locations into json files
# Be careful with encoding and no ascii ensure
with open('locations.json', 'w', encoding='utf-8') as f:
    json.dump(locations, f, ensure_ascii=False)
