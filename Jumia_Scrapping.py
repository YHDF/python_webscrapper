import requests
import bs4
from product import products
import initialize

link_start = 'https://www.jumia.ma/'

def phone_scrap(initi, counter):
    if(counter >=  40):
        return None
    if(initi.section[counter].getText() == ""):
        counter += 1
    name = initi.section[counter].select_one('.name')
    price = initi.section[counter].select_one('.prc')
    product_link = initi.section[counter].select_one('.core')

    product_link = link_start + product_link['href']
    img_link = initi.section[counter].select_one('.img-c img')['data-src']
    name = name if not None else 'N/a'
    price = price if price is not None else 'N/a'
    obj = products(name if name == 'N/a' else name.getText(), price if price == 'N/a' else price.getText(), img_link, product_link)
    return obj
