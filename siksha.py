from requests import Session
from bs4 import BeautifulSoup as BS
import pandas as pd
from lxml import html
from pymongo import MongoClient

s = Session()
s.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
x = []

URI = "mongodb://localhost:27017"
Client = MongoClient(URI)
mydb = Client['crawling']
mycol = mydb['Siksha']


def crawl_list(cat_url):
    r = s.get(cat_url)
    soup = BS(r.text,'html.parser')
    tree = html.fromstring(r.text)
    js = r.json()
    pro = js['data']['paginationData']
    
    curtpage = js['data']['tupleRequest'].get('url')
    currunt_page='https://www.shiksha.com'+curtpage
    x.append(currunt_page)

    for page in pro.get('nextUrls'):
        urls = 'https://www.shiksha.com'+page.get('url')
        x.append(urls)

    for i in pro.get('prevUrls'):
        previews = 'https://www.shiksha.com'+i.get('url')
        x.append(previews)
    
    # print(x)

def craw_list_page(url):
    r = s.get(url)
    print(r.url)
    soup = BS(r.text,'html.parser')
    tree = html.fromstring(r.text)

    product = soup.find_all('div','_8165')
    for pro in product:
        title = pro.find('div','c43a').get('title')

        try:
            links = 'https://www.shiksha.com'+pro.find('a','ripple dark').get('href')
        except:
            links = 'https://www.shiksha.com'+pro.find('a','_9865 ripple dark').get('href')
        
        location = pro.find('div','edfa').find('span').text
    
        try:
            course = pro.find('a','_9865 ripple dark').text
        except:
            course = ''
        try:
            rating = pro.find('a','_68c4 ripple dark').text
        except:
            rating = ''
        try:
            exams = pro.find('ul','_0954').text
        except:
            exams = ''

        for fee in pro.find_all('div','_77ff'):
            if fee.find('label').text.strip()=='Total Fees Range':
                try:
                    total_fee = fee.find('div').text.strip()
                except:
                    total_fee= ''
            elif fee.find('label').text.strip()=='Value for Money Rating':
                try:
                    total_fee = fee.find('div').text.strip()+'Value for Money Rating'
                except:
                    total_fee= ''
            else:
                total_fee = ''
    
        for avarage in pro.find_all('div','_77ff'):
            if avarage.find('label').text.strip()=='Average Package':
                try:
                    Avarage_packege = avarage.find('div').text.strip()
                except:
                    Avarage_packege = ''
            elif avarage.find('label').text.strip()=='Placement Rating':
                try:
                    Avarage_packege = avarage.find('div').text.strip()+'Placement Rating'
                except:
                    Avarage_packege = ''
            else:
                Avarage_packege = ''

        

        
        item = dict()
        item['title'] = title 
        item['location'] = location 
        item['Course'] = course 
        item['Rating'] = rating 
        item['Exams_accepted'] = exams 
        item['Total_fees'] = total_fee 
        item['Packages'] = Avarage_packege 
        item['links'] = links 
        print(item)

        try:
            mycol.insert_one(item)
        except:
            pass



crawl_list("https://apis.shiksha.com/apigateway/categorypageapi/v2/info/getCategoryPageFull?data=eyJyZiI6InNlYXJjaFdpZGdldCIsImxhbmRpbmciOiJjdHAiLCJ1cmwiOiIvZW5naW5lZXJpbmcvY29sbGVnZXMvYi10ZWNoLWNvbGxlZ2VzLWluZGlhLTQiLCJmciI6InRydWUiLCJmZXRjaFBDVyI6dHJ1ZX0=")

for row in x:
    craw_list_page(row)