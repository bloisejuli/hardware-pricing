import requests
import lxml.html.soupparser as sp


def get_page_from_url(url: str):
    
    session = requests.Session()

    response = session.get(url, headers={
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                    'Chrome/44.0.2403.157 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    })
    data = response.content.decode('utf-8')

    return data

def get_page_parsed(url: str):

    page = get_page_from_url(url)
    parsed_page = ''

    parsed_page = sp.fromstring(page)


    return parsed_page

page = get_page_parsed("https://www.maximus.com.ar/")

categories = page.xpath("//li[@class='componentes-sidebar']/div/a")
print(categories)

for category in categories:
    print(category.get("href"))