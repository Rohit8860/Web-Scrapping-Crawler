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
mycol = mydb['jeevansathi.com'] ## collection


def crawl_list(url):
    page = 1
    while True:
        r = s.get(url.format(page))
        print(r.url)
        js = r.json()['profiles']
        if len(js)==0:
            break

        for pro in js:
            user_login_status = pro['userloginstatus']
            subcription = pro['subscription_text']
            age = pro['age']
            height = pro['height']
            caste = pro['caste']
            income = pro['income']
            m_tongue = pro['mtongue']
            edu = pro['edu_level_new']
            location = pro['location']
            current_location = pro['current_location']
            religion = pro['religion']
            gender = pro['gender']
            m_status = pro['mstatus']
            college = pro['college']
            pg_college = pro['pg_college']
            company_name = pro['company_name']
            profileid = pro['profileid']
            
            try:
                verification = pro['verification_data'].get('Self')
            except:
                verification =""

            try:
                sub_catse = pro['subcaste']
            except:
                sub_catse = ""

            item = dict()
            item['_id'] = profileid
            item['height'] = height
            item['caste'] = caste
            item['sub_catse'] = sub_catse
            item['age'] = age
            item['subcription'] = subcription
            item['gender'] = gender
            item['user_login_status'] = user_login_status
            item['location'] = location
            item['current_location'] = current_location
            item['religion'] = religion
            item['edu'] = edu
            item['Verification_data'] = verification
            item['m_tongue'] = m_tongue
            item['income'] = income
            item['m_status'] = m_status
            item['college'] = college
            item['pg_college'] = pg_college
            item['company_name'] = company_name
            print(item)

            try:
                mycol.insert_one(item)
            except:
                pass

        page += 1


crawl_list("https://www.jeevansathi.com/api/v1/search/perform?searchsrc=srp1&searchId=167467095243435751&results_orAnd_cluster=onlyResults&currentPage={}&searchBasedParam=quicksearchband")