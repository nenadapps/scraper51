from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

base_url = 'https://www.herrickstamp.com'

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(html, subcategory, stamp_url):
    
    stamp = {}
    
    try:
        raw_text = html.select('.prod_result_titleprice')[0].get_text().strip()
        raw_text = raw_text.replace(u'\xa0', u' ')
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
   
    try:
        price = html.select('.price')[0].get_text().strip()
        price = price.replace('Price: $', '').strip()
        
        if 'Price' in price:
            price_parts1 = price.split('$')
            price_parts2 = price_parts1[1].split('Price')
            price = price_parts2[0]
        
        stamp['price'] = price
    except:
        stamp['price'] = None  
    
    stamp['category'] = 'country-stamps'
    stamp['subcategory'] = subcategory
    
    stamp['currency'] = 'USD'
    
    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('img')
        for image_item in image_items:
            img = base_url + image_item.get('src')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = stamp_url
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''
    
    try:
        html = get_html(url)
    except:
        return items, next_url
    
    try:
        for item in html.select('.listprod'):
            if item not in items:
                items.append(item)
    except:
        pass
    
    try:
        for next_item in html.select('form a'):
            next_text = next_item.get_text().strip()
            if next_text == 'Next':
                 next_url = base_url + next_item.get('href')
                 break
    except:
        pass
   
    shuffle(list(set(items)))
    
    return items, next_url

def get_subcategories():
    
    url = 'https://www.herrickstamp.com/country-stamps'
   
    items = {}

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('.container .col-md-4 a'):
            item_link = base_url + item.get('href')
            item_text = item.get_text().strip()
            if (item_link not in items) and (item_text != 'Stamps'): 
                items[item_text] = item_link
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items

subcategories = get_subcategories()   
for subcategory in subcategories:
    page_url = subcategories[subcategory]
    while(page_url):
        page_items, page_url = get_page_items(page_url)
        for page_item in page_items:
            stamp = get_details(page_item, subcategory, subcategories[subcategory]) 
