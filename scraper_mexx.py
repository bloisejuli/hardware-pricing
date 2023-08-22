import requests
import lxml.html.soupparser as sp
import pandas
from my_sql_connector import create_engine_mysql
import datetime

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
    title = get_text_or_not_found(item.xpath(".//h4/a"))
    link = item.xpath("div/div[contains(@class,'overlay')]/a/@href")[0]
    price_elements = item.xpath(".//div[contains(@class, 'price')]/h4/b")
    cash_price = get_text_or_not_found(price_elements)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "category": category,
        "title": title,
        "cash_price": cash_price,
        "link": link,
        "created_at": current_date
    }


if __name__ == '__main__':
    categories = ['notebooks', 'motherboards', 'memorias-ram', 'procesadores','almacenamiento','placas-de-video','fuentes-de-poder','gabinetes','refrigeracion-pc','combos-actualizacion-pc','teclados-mouses-y-pads','auriculares-y-microfonos-','camaras-web-e-ip','monitores','conectividad-y-redes','volantes-y-gamepads','outlet']
    data_list = []


    for category in categories:
        page = get_page_parsed(f'https://www.mexx.com.ar/productos-rubro/{category}/?all=1')
        items = page.xpath("//div[contains(@class,'productos')]")
        for item in items:
            data = extract_data(item, category)
            data_list.append(data)
            

    myvar = pandas.DataFrame.from_records(data_list)
    print(myvar)

    engine = create_engine_mysql()

    try:
        myvar.to_sql("products", con=engine, if_exists='append', index=False)
        print("Datos insertados en la base de datos.")
    except Exception as e:
        print("Error:", e)
