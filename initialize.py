import requests
import bs4
class initial:
    section = None
    count = 0

initial_obj = initial()

def init(page_number,url, atr):
    res = []

    while True:
        querystr = url
        string = querystr + str(page_number)
        headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
        }
        res = requests.get(string, headers=headers)
        bs = bs4.BeautifulSoup(res.text, 'lxml')
        section = bs.select(atr)
        if(section != []):
            break
    count = len(section) - 1
    initial_obj.section = section
    initial_obj.count = count
    print(count)
    return initial_obj
