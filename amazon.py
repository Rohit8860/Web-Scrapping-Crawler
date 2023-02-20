from lxml import html
from bs4 import BeautifulSoup as BS
import pandas as pd
import requests
import re
from requests import Session
import time
import random
product = []
s = Session()
s.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'


def crawl_details(cat_url):
    # r = s.get(url,headers=headers)
    time.sleep(random.randrange(1,10))
    response = requests.get(cat_url)
    # soup = BS(r.text,'html.parser')

    tree = html.fromstring(response.text)
    try:
        display = ''.join(tree.xpath('//table[@class="a-bordered"]//td/p[strong and contains (string(),"Display")]/parent :: td/following-sibling :: td//p/text()'))
    except:
        display = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Standing screen display size")]/following-sibling::td//text()')).strip().replace("\u200e","").replace("\n","")

    try:

        name = "".join(tree.xpath('//span[@id="productTitle"]/text()')).strip()
    except:
        name = ''.join(tree.xpath('//span[@class="a-size-large product-title-word-break"]/text()')).strip()

    try:
        list_price = ''.join(tree.xpath('//span[@class="a-price a-text-price"]//span[@class="a-offscreen"]/text()'))
    except:
        list_price=     ''.join(tree.xpath('//td[@class="a-span12 a-color-secondary a-size-base"]//span[@class="a-price a-text-price a-size-base"]//span[@class="a-offscreen"]/text()'))
    try:
        price = ''.join(tree.xpath('//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]//span[@class="a-offscreen"]/text()'))
    except:
        price = ''.join(tree.xpath('//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]//span[@class="a-offscreen"]/text()'))
    description = ''.join(tree.xpath('//ul[@class="a-unordered-list a-vertical a-spacing-mini"]//span[@class="a-list-item"]/text()'))
    try:
        colour = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Colour")]/following-sibling::td//text()')).strip().replace("\u200e","")
    except:
        colour = "".join(tree.xpath('//span[@class="a-size-base a-text-bold" and contains(string(),"Colour")]/parent::td/following-sibling::td//text()')).strip()
    
    battery = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Batteries ")]/following-sibling::td//text()')).strip().replace("\u200e","").replace("\n","").replace("Yes","")
    try:
        processer = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Processor Brand ")]/following-sibling::td//text()')).strip().replace("\u200e","")
           
    except:
        try:
            processer = ''.join(tree.xpath('//table[@class="a-bordered"]//td/p[strong and contains (string(),"Processor")]/parent :: td/following-sibling :: td//p/text()'))
        except:
            processer= ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[contains(string(),"Processor Brand")]//following-sibling::td//text()')).strip().replace("\u200e","")
            
    try:
        processer_type = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Processor Type ")]/following-sibling::td//text()')).strip().replace("\u200e","")
    except:
        processer_type = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[contains(string(),"Processor Type ")]//following-sibling::td//text()')).strip().replace("\u200e","")

    processer_speed = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Processor Speed")]/following-sibling::td//text()')).strip().replace("\u200e","")
    hard_disk = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Hard Disk Description")]/following-sibling::td//text()')).strip().replace("\u200e","")
    try:
        grafic = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Graphics Coprocessor ")]/following-sibling::td//text()')).strip().replace("\u200e","")
           
    except:
        try:
            grafic = ''.join(tree.xpath('//table[@class="a-bordered"]//td/p[strong and contains (string(),"Graphics")]/parent :: td/following-sibling :: td//p/text()'))
        except:
            grafic = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[contains(string(),"Graphics Chipset Brand")]//following-sibling::td//text()')).strip().replace("\u200e","") 

    try:
        brand = tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Brand ")]/following-sibling::td//text()')[0].replace("\u200e","").replace("\n","").strip()     
    except:
        try:
            brand =''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Brand ")]/following-sibling::td//text()')).strip().replace("\u200e","").strip().replace("\n","").replace("Intel","").strip()
        except:
            brand = "".join(tree.xpath('//span[@class="a-size-base a-text-bold" and contains(string(),"Brand")]/parent::td/following-sibling::td//text()')).strip()
            
                

    operating = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Operating System")]/following-sibling::td//text()')).strip().replace("\u200e","")
    
    grafic_ram = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[@class="a-color-secondary a-size-base prodDetSectionEntry" and contains(string(),"Graphics RAM Type")]/following-sibling::td//text()')).strip().replace("\u200e","")
    
    try:
        ram = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[contains(string(),"Maximum Memory Supported")]//following-sibling::td//text()')).strip().replace("\u200e","")
    except:
        try:
            ram = ''.join(tree.xpath('//table[@id="productDetails_techSpec_section_1"]//th[contains(string(),"RAM Size")]//following-sibling::td//text()')).strip().replace("\u200e","")
        except:
            ram = "".join(tree.xpath('//span[@class="a-size-base a-text-bold" and contains(string(),"RAM Memory")]/parent::td/following-sibling::td//text()')).strip()
    
    urls = ''.join(tree.xpath('//link[@rel="canonical"]/@href'))
    l = []
    for key in tree.xpath('//span[@class="a-button-inner"]//span[@class="a-button-text"]//img/@src'):
        if not key.endswith('gif'):
            l.append(key.replace("SS40","SS900").replace("SS64","SS900"))
           


    item = dict()
    item['name'] = name
    item['Brand'] = brand
    item['Off_price'] = list_price
    item['price'] = price
    item['Ram'] = ram    
    item['Colour'] = colour
    item['Display'] = display
    item['processer_type'] = processer_type
    item['processer'] = processer
    item['battery'] = battery
    item['processer_speed'] = processer_speed
    item['hard Disk'] = hard_disk
    item['Grafic'] = grafic
    item['operating System'] = operating
    item['grafic_ram'] = grafic_ram
    item['description'] = description
    item['Image'] = l
    item['Url'] = urls

    print(item)
    product.append(item)



df = pd.read_excel('xpath_in.xlsx')

for i in range(len(df)):
    row = df.iloc[i].to_dict()

    url = row['link']
    crawl_details(url)

df = pd.DataFrame(product)
df.to_excel('amazon_in.xlsx')