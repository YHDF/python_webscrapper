import requests
import bs4
from product import products



def phone_scrap(initi, counter):
    name = initi[counter].select_one('li h3')
    price = initi[counter].select_one('li .s-item__price')
    product_link = initi[counter].select_one('li .s-item__link')['href']
    name = name if not None else 'N/a'
    price = price if price is not None else 'N/a'
    img_link = initi[counter].select_one('li .s-item__image-img')['data-src']  if initi[counter].select_one('li .s-item__image-img')['src'] == 'https://ir.ebaystatic.com/cr/v/c1/s_1x2.gif' else initi[counter].select_one('li .s-item__image-img')['src']
    obj = products(name.getText(), price.getText(), img_link, product_link)
    return obj
