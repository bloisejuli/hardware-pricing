import requests
import lxml.html.soupparser as sp
import pandas
import datetime
from my_sql_connector import create_engine_mysql

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

    data = response.content.decode('utf-8', 'replace')
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
    title = get_text_or_not_found(item.xpath(".//h3/a"))
    link = item.xpath("//h3/a/@href")[0]
    price_elements = item.xpath(".//span[@class='current-price']")
    cash_price = get_text_or_not_found(price_elements)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "category": category,
        "title": title,
        "cash_price": cash_price,
        "link": link,
        "created_at": current_date
    }

def extract_data_from_categories(data_list, categories, url):
    for category in categories:
        page = get_page_parsed(f'{url}/{category}?limit=96')
        items = page.xpath("//div[contains(@class,'product')]/div/div")
        
        if category == 'precios-explosivos':
            category = 'outlet'
        
        for item in items:
            data = extract_data(item, category)
            data_list.append(data)


if __name__ == '__main__':

    url = "https://www.venex.com.ar/"
    categories = ['notebooks', 'monitores', 'precios-explosivos']
    components = ['placas-de-video', 'memorias-ram']
    
    data_list = []

    extract_data_from_categories(data_list, categories, url)
    extract_data_from_categories(data_list, components, url + '/componentes-de-pc')

    df = pandas.DataFrame.from_records(data_list)
    print(df)

    df.drop(df[(df["cash_price"] == 'Not found')].index, inplace=True)
    print(df)
    engine = create_engine_mysql()
    
    try:
        df.to_sql("products", con=engine, if_exists='append', index=False)
        print("Datos insertados en la base de datos.")
    except Exception as e:
        print("Error:", e)

