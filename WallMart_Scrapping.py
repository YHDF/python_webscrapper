import requests
import bs4
from product import products
import initialize
import re


def phone_scrap(initi, counter):
	name = initi[counter].select_one('.product-title-link span')
	decimal = initi[counter].select_one('.price-characteristic')
	floatpoint = initi[counter].select_one('.price-mantissa')
	price ='$' + decimal.getText() if decimal is not None else '' + '.' + floatpoint.getText() if floatpoint is not None else ''
	product_link = initi[counter].select_one('.product-title-link')['href']
	img_link = initi[counter].select_one('.orientation-square img')['src']
	rating = initi[counter].select_one('.stars-reviews-count span')
	obj = products(name.getText(), price, img_link, product_link)
	return obj
