from lxml import html
from bs4 import BeautifulSoup as BS
import pandas as pd
import requests
import re
from requests import Session
import time
import random
from pymongo import MongoClient

s = Session()
s.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'

URI = "mongodb://localhost:27017"
client = MongoClient(URI)
mydb = client['crawling'] ## database
mycol = mydb['Naukari.com'] ## collectio


import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.99acres.com/search/property/rent/flat?city=1075722&keyword=flat&preference=R&area_unit=1&res_com=R',
    'AuthorizationToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiOHFhTEJhZ0JXb1lmUCtFVWE1SURwYUVLbzdVY0pEQlBLemhBYWtMOGN1Rjk2NzZKWmlyWmFzbW1BcHhtVkZETnVqU1VaVHNYVk9XRlNxc2RQckdKRDVyNDU1Q3gvUlZxQjlCc0puY1lLcFBlN3AwWmVvTDFOczFNUldlSlRHYnBpczRRQjVWWjZTTUtzdEwrYWRhRzdnPT0iLCJpYXQiOjE2NzUwMTU0MDEsImV4cCI6MTY3NTAxNjAwMX0.B5zv42osEE3qiuZlr4hFO-bOeHO-SNimwNVZ2JsFSiM',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
    'Cookie': '99_ab=34; GOOGLE_SEARCH_ID=2685891674732921023; __utma=267917265.1479601710.1674732924.1674735752.1675015297.3; __utmz=267917265.1675015297.3.2.utmgclid=Cj0KCQiAz9ieBhCIARIsACB0oGLyz9wsC-saTnCdiLBjrDwCX6HOQHDwfGd0xe_frOkgSPZB6L05Ys4aAtbjEALw_wcB^|utmccn=(not^%^20set)^|utmcmd=(not^%^20set)^|utmctr=(not^%^20provided); _gac_UA-224016-1=1.1675015298.Cj0KCQiAz9ieBhCIARIsACB0oGLyz9wsC-saTnCdiLBjrDwCX6HOQHDwfGd0xe_frOkgSPZB6L05Ys4aAtbjEALw_wcB; _gcl_aw=GCL.1675015297.Cj0KCQiAz9ieBhCIARIsACB0oGLyz9wsC-saTnCdiLBjrDwCX6HOQHDwfGd0xe_frOkgSPZB6L05Ys4aAtbjEALw_wcB; _gcl_au=1.1.1204941406.1674732924; _ga=GA1.2.1479601710.1674732924; _hjSessionUser_3171461=eyJpZCI6Ijk4M2RkNWJlLTBlNmMtNTEzMC1iYjdkLTkzNWY3M2NiN2I2YiIsImNyZWF0ZWQiOjE2NzQ3MzI5MjQ4NzEsImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1674732925721.388645500; 99_suggestor=15; hp_bcf_data=; _sess_id=t^%^2FjmtYirt^%^2BrUeXg3Ya^%^2Brf7bzVEFeywLIxFd9NxhEjyrODNSp2oppo4AlOiGLI35Z1oOs2A5blHu^%^2FR83G1PY3EQ^%^3D^%^3D; session_source=https://www.google.com/; __utmb=267917265.3.10.1675015297; __utmc=267917265; __utmt=1; _gid=GA1.2.1449740721.1675015298; ln_or=eyIyNDkxNDYiOiJkIn0^%^3D; _hjIncludedInSessionSample=0; _hjSession_3171461=eyJpZCI6IjgzOGEyZDI2LTkzNTYtNGQ2Zi05MmQwLTg4ZDU4MzhiOGY1MiIsImNyZWF0ZWQiOjE2NzUwMTUyOTg0NDgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; outbrain_cid_fetch=true; landmark_toast=true; 99_FP_VISITOR_OFFSET=73; _sess_id=t^%^2FjmtYirt^%^2BrUeXg3Ya^%^2Brf7bzVEFeywLIxFd9NxhEjyrODNSp2oppo4AlOiGLI35Z1oOs2A5blHu^%^2FR83G1PY3EQ^%^3D^%^3D',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}


def crawl_api(url):
    page = 0
    while True:
        params = {
            'page': str(page),
            'page_size': '25',
            'platform': 'DESKTOP',
            'encrypted_input': 'UiB8ICB8IFIgIzE0I3wgIHwgMSB8IDEwNzU3MjIgfCMxIyAgfCAyNSM0IyB8IDI4LjYzNTMxIHwgNzcuMjI0OTYgfCMyOSMgIHwgRlJFRV9URVhUIHwgMzQgfCBGUkVFX1RFWFQjMTEjIHwgMCB8IGZhbHNlIzMyIyB8IFkgfCMzMyMgIHwgZmFsc2UjMSMgfCBmYWxzZSB8ICB8IE4jMiMgfCBmYWxzZSB8IGZhbHNlIHwjNCMgIHwgRU5ESU5HIHwg',
            'recomGroupType': 'VSP',
            'pageName': 'SRP',
            'search_type': 'QS',
            'groupByConfigurations': 'true',
        }

        response = requests.get(url, params=params, headers=headers)
        print(response.url)
        r = s.get(url.format(page))
        # print(r.url)
        js = r.json()['properties']
        if len(js)==0:
            break


        for pro in js:
            PRofile_id = pro['PROFILEID']
            PROP_ID = pro['PROP_ID']
            a = pro['DESCRIPTION']
            description = BS(a,'html.parser').text
            property_type = pro['PROPERTY_TYPE']
            city = pro['CITY']
            locality = pro['LOCALITY']
            BEDROOM_NUM = pro['BEDROOM_NUM']
            BATHROOM_NUM = pro['BATHROOM_NUM']
            BALCONY_NUM = pro['BALCONY_NUM']
            FLOOR_NUM = pro['FLOOR_NUM']
            PROP_NAME = pro['PROP_NAME']
            MIN_PRICE = pro['MIN_PRICE']
            MAX_PRICE = pro['MAX_PRICE']
            PROPERTY_NUMBER = pro['PROPERTY_NUMBER']
            PRICE = pro['PRICE']
            PROP_HEADING = pro['PROP_HEADING']
            PROP_DETAILS_URL = pro['PROP_DETAILS_URL']


            try:
                PROPERTY_IMAGES = pro['PROPERTY_IMAGES']
            except:
                PROPERTY_IMAGES = ""
            
            row = {
                'PROP_ID':PROP_ID,'PROP_NAME':PROP_NAME,'PROP_HEADING':PROP_HEADING,'PROPERTY_NUMBER':PROPERTY_NUMBER,'PRICE':PRICE,
                'MIN_PRICE':MIN_PRICE,'MAX_PRICE':MAX_PRICE,'property_type':property_type,'city':city,'locality':locality,'_id_PRofile':PRofile_id,
                'FLOOR_NUM':FLOOR_NUM,'BEDROOM_NUM':BEDROOM_NUM,'BATHROOM_NUM':BATHROOM_NUM,'BALCONY_NUM':BALCONY_NUM,
                'description':description,'PROPERTY_IMAGES':PROPERTY_IMAGES,'PROP_DETAILS_URL':PROP_DETAILS_URL
                }
        
            # print(row)
        page +=1



crawl_api("https://www.99acres.com/api-aggregator/discovery/srp/search?page={}&page_size=25&platform=DESKTOP&encrypted_input=UiB8IFFTIHwgUiB8IzE0IyAgfCAxIHwgMTA3NTcyMiMyIyB8IDI1ICMzI3wgIHwgMjguNjM1MzEgfCA3Ny4yMjQ5NiMzMCMgfCBGUkVFX1RFWFQgfCAzNCB8IEZSRUVfVEVYVCAjMTAjfCAgfCAwIHwgZmFsc2UgIzMxI3wgIHwgWSMzNCMgfCBmYWxzZSB8ICB8IGZhbHNlIHwgIHwgTiAjMSN8ICB8IGZhbHNlIHwgZmFsc2UjNSMgfCBFTkRJTkcgfCA=&recomGroupType=VSP&pageName=SRP&search_type=QS&groupByConfigurations=true")
# a =      ("https://www.99acres.com/api-aggregator/discovery/srp/search?page=2 &page_size=25&platform=DESKTOP&encrypted_input=UiB8ICB8IFIgIzE0I3wgIHwgMSB8IDEwNzU3MjIgfCMxIyAgfCAyNSM0IyB8IDI4LjYzNTMxIHwgNzcuMjI0OTYgfCMyOSMgIHwgRlJFRV9URVhUIHwgMzQgfCBGUkVFX1RFWFQjMTEjIHwgMCB8IGZhbHNlIzMyIyB8IFkgfCMzMyMgIHwgZmFsc2UjMSMgfCBmYWxzZSB8ICB8IE4jMiMgfCBmYWxzZSB8IGZhbHNlIHwjNCMgIHwgRU5ESU5HIHwg&recomGroupType=VSP&pageName=SRP&search_type=QS&groupByConfigurations=true")