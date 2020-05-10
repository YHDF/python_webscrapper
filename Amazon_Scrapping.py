import requests
import bs4
from product import products
import initialize

link_start = 'https://amazon.com'


def phone_scrap(initi, counter):
    if counter == 0:
        return None
    name = initi[counter].select_one('a span')
    if(name is not None):
        result1 = name.getText().find('Best Seller')
        result2 = name.getText().find('Amazon')
        if(result1 != -1 or result2 != -1):
            return None
    price = initi[counter].select_one('.a-color-secondary .a-color-base')
    img = initi[counter].select_one('.s-image')
    if(img is None):
        img_link = ''
    else:
        img_link = img['src']
    rating = initi[counter].select_one('.a-size-base')
    link  = link_start + initi[counter].select_one('.a-link-normal')['href']
    name = name if price is not None else 'N/a'
    price = price if price is not None else 'N/a'
    obj = products(name if name == 'N/a' else name.getText(), price if price == 'N/a' else price.getText(), img_link, link)
    return obj