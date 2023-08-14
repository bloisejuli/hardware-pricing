"""
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


def get_json_data_from_script(parsed_page):
    scripts = parsed_page.xpath("//script[contains(text(), 'wsNRW_Script')]")
    print("QUE PASA ACA")
    print(type_of(scripts))
    if scripts:
        print("entre?")
        script_text = scripts[0].text
        print(script_text)
        start_index = script_text.find('"d": "') + 6
        end_index = script_text.find('"}', start_index) + 1
        json_data = script_text[start_index:end_index]
        print(json_data)
        return json_data
    return None

def get_items_from_json(json_data):
    data = json.loads(json_data)
    items = data["data"]["items"]
    return items


categories = page.xpath("//li[@class='componentes-sidebar']/div/a")
print(len(categories))

for category in categories:
    url_category = category.get("href")
    if ('Notebooks' in url_category):
        print("HOLA")
        page_category = get_page_parsed(url_category)
        #products = page_category.xpath('//div[@id="articulos"]//div[@class="product"]')
        json_data = get_json_data_from_script(page_category)
        if json_data:
            print("chau") 
            items = get_items_from_json(json_data)
            for item in items:
                print("EN ITEMS")
                print("Item ID:", item["item_id"])
                print("Item Description:", item["item_desc"])
                print("Price:", item["prli_price"])
                print("Original Price:", item["prli_price_original"])
"""
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
def obtain_url_categories():
    page = get_page_parsed("https://www.maximus.com.ar/")
    categories = page.xpath("//li[@class='componentes-sidebar']/div/a")
    url_category = []
    for category in categories:
        url_category.append(category.get("href"))
    return url_category
