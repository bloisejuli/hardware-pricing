import requests
import lxml.html.soupparser as sp
import csv
import pandas
from my_sql_connector import create_engine

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


def get_text_or_not_found(elements):
    if elements:
        return elements[0].text
    else:
        return "Not found"

def extract_data(item,category):
    discount_applied = get_text_or_not_found(item.xpath("span"))
    product = get_text_or_not_found(item.xpath(".//h4/a"))
    link = item.xpath("div/div[contains(@class,'overlay')]/a/@href")[0]
    price_elements = item.xpath(".//div[contains(@class, 'price')]/h4/b")
    discount_price = get_text_or_not_found(price_elements)
    #price = 


    return {
        "Category": category,
        "Discount": discount_applied,
        "Product": product,
        "Discount_Price": discount_price,
        "Link": link
    }

def print_data(data_list):
    for item_data in data_list:
        print("Discount:", item_data["Discount"])
        print("Product:", item_data["Product"])
        print("Price:", item_data["Discount_Price"])
        print("Link:", item_data["Link"])
        print("-" * 20)

url_base = 'https://www.mexx.com.ar/productos-rubro/{}/?all=1'

categories = ['notebooks', 'motherboards', 'memorias-ram', 'procesadores','almacenamiento','placas-de-video','fuentes-de-poder','gabinetes','refrigeracion-pc','combos-actualizacion-pc','teclados-mouses-y-pads','auriculares-y-microfonos-','camaras-web-e-ip','monitores','conectividad-y-redes','volantes-y-gamepads','outlet']


data_list = []


for category in categories:
    page = get_page_parsed(f'https://www.mexx.com.ar/productos-rubro/{category}/?all=1')
    items = page.xpath("//div[contains(@class,'productos')]")
    #print("AAAAAAAAAAAAAAAAAAAAAAA")
    #print(f'https://www.mexx.com.ar/productos-rubro/{category}/?all=1')
    for item in items:
        data = extract_data(item, category)
        data_list.append(data)
        
#print_data(data_list)


myvar = pandas.DataFrame.from_records(data_list)
connection = create_engine()
myvar.to_sql("products", connection, if_exists = 'append', index = False)
print(myvar)