import requests
import bs4
from product import products
import initialize

link_start = 'https:'

def phone_scrap(initi, counter):
    if(initi.section[counter].getText() == ""):
        counter += 1
    name = initi.section[counter].select_one('.name')
    price = initi.section[counter].select_one('.price span')
    product_link = initi.section[counter].select_one('.link')['href']
    img_link = initi.section[counter].select_one('.image-wrapper .image')['data-src']
    rating = initi.section[counter].select_one('.total-ratings')
    name = name if not None else 'N/a'
    price = price if price is not None else 'N/a'
    obj = products(name if name == 'N/a' else name.getText(), price if price == 'N/a' else price.getText(), img_link, product_link)
    return obj
