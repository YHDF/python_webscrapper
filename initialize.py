import requests
import bs4
class initial:
  section = None
  count = 0
	
initial_obj = initial()

def init(page_number,url, atr):
    res = []
    session_token_str = 'oOrRQLccBzzInSeWD6LC' + '%' + '2FMRZpPjhwIN' + '%'+ '2F'+ '%'+'2FOQdCeaI'+ '%'+'2Fk6YWosR5EBuj1Z%2BZOEbF7cMTKRmRze1xiojPT3'+'%'+'2FoJAfRZjlCrpPn1m9NtYFXWB9hjjDNW' + '%' +'2Fb%2BE6g6Ru' + '%' +'2FX5nyqs42%2BC6Mt9VjZ9dq' + '%' +'2FZ0KjQ%2B3msPx44em27dPzS5oLLf6aNdKygjStyBrSBshClUhq%2B0D'
    #url_amazon_computers = 'https://www.amazon.com/s?k=computers&i=computers&rh=n%3A172282%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565108&dc&qid=1588790979&swrs=294E4AC6A8E6CE5E79B377B7F9CA77D9&ref=sr_pg_2&page='
    url_amazon_phones = 'https://www.amazon.com/s?k=smartphones&qid=1588556990&ref=sr_pg_2&page='
    while True:
        querystr = url
        string = querystr + str(page_number)
        headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
        }
        jar = requests.cookies.RequestsCookieJar()
        if(url == url_amazon_phones): #or url == url_amazon_computers
            jar.set('session-token', session_token_str, domain='amazon.com', path='/')
            res = requests.get(string, headers=headers, cookies=jar)
        else : 
            res = requests.get(string, headers=headers)
        bs = bs4.BeautifulSoup(res.text, 'lxml')
        section = bs.select(atr)
        if(section != []):
            break;
    count = len(section) - 1
    initial_obj.section = section
    initial_obj.count = count
    print(count)
    return initial_obj
