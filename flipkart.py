from requests import Session
from bs4 import BeautifulSoup as BS
import pandas as pd
from lxml import html
s = Session()
s.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'


base_url = "https://www.flipkart.com{}"
pagination_url = "&page={}"
listpage =[]
def crawl_sub(url):
    r = s.get(url)
    tree = html.fromstring(r.text)
    soup = BS(r.text,'html.parser')

    h = []
    main_cat_url = tree.xpath('//a[@class="_2KpZ6l _3dESVI"]/@href')
    for i in main_cat_url:
        h.append(base_url.format(i))
    # print(h)

    for page in h:
        r = s.get(page)
        soup = BS(r.text,'html.parser')
        # print('main url page',page)
        page_count = int(soup.find('div','_2MImiq').find('span').text.strip('Page').strip('1 of'))
        # print(page_count)
        if page_count:
            for num in range(1,page_count+1):
                # print(num)
                list_page_url= page + pagination_url.format(num)
                # print('url ------',list_page_url)
                crawl_list(list_page_url)
        else:
            page_count = 1    


def crawl_list(cat_url):
    r = s.get(cat_url)
    tree = html.fromstring(r.text)
    soup = BS(r.text,'html.parser')
    

    pro = tree.xpath('//div[@class="_1AtVbE col-12-12"]//div[@class="_2kHMtA"]')
    for i in pro:
        price = ''.join(i.xpath('.//div[@class="_30jeq3 _1_WHN1"]/text()'))
        # off_price = ''.join(i.xpath('.//div[@class="_3I9_wc _27UcVY"]/text()')).replace("₹","")
        off_price = '  '.join(tree.xpath('//div[@class="_3I9_wc _27UcVY"]/text()')).replace("'₹'","").strip().replace("₹","")
        links ='https://www.flipkart.com'+' '.join(i.xpath('.//a[@class="_1fQZEK"]/@href'))

        product_links.append({'price':price,'Off_price':off_price,'url':links})    

def crawl_details(row):
    url = row.get('url')
    price = row.get('price')
    off_price = row.get('off_price')


    r = s.get(url)
    soup = BS(r.text,'html.parser')
    tree = html.fromstring(r.text)

    title = ''.join(tree.xpath('//span[@class="B_NuCI"]/text()'))
    try:
        ram = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"Dedicated Graphic Memory Capacity")]/following-sibling::td//ul//li/text()'))
    except:
        ram = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"RAM")]/following-sibling::td//ul//li/text()'))[0]

    processer_brand = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"Processor Brand")]/following-sibling:: td//ul//li/text()'))
    processer_name = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"Processor Name")]/following-sibling:: td//ul//li/text()'))
    processer_generation = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"Processor Generation")]/following-sibling:: td//ul//li/text()'))
    storage = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"SSD Capacity")]/following-sibling:: td//ul//li/text()'))
    screen_size = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"Screen Size")]/following-sibling:: td//ul//li/text()'))
    image = ' , '.join(tree.xpath('//img[@class="q6DClP"]/@src')).replace("128","720")
    model_name  = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"Model Name")]/following-sibling:: td//ul//li/text()'))
    try:
        operating_system = tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"Operating System")]/following-sibling:: td//ul//li/text()')[0]
    except:
        operating_system = ""
    
    colour = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"Color")]/following-sibling:: td//ul//li/text()'))
    item = dict()

    
    grafic = ''.join(tree.xpath('//tr[@class="_1s_Smc row"]//td[@class="_1hKmbr col col-3-12" and contains (string(),"Graphic Processor")]/following-sibling:: td//ul//li/text()'))
   
    item['Title'] = title
    item['model_name'] = model_name
    item['Price '] = price
    item['Off_price'] = off_price
    item['ram'] = ram
    item['Colour'] = colour
    item['processer_brand'] = processer_brand
    item['processer_name'] = processer_name
    item['processer_generation'] = processer_generation
    item['storage'] = storage
    item['Grafic'] = grafic
    item['operating_system'] = operating_system
    item['screen_size'] = screen_size
    item['Image'] = image
    item['product_url'] = url
    products_detail.append(item)
    print(item)


product_links = []
products_detail = []
crawl_sub("https://www.flipkart.com/laptops-store?otracker=nmenu_sub_Electronics_0_Laptops")
for row in product_links:
    crawl_details(row)

df = pd.DataFrame(products_detail)
df.to_excel("flipkart_in.xlsx")