import pandas
import datetime
from my_sql_connector import create_engine_mysql
from web_utils import get_text_or_not_found, get_page_parsed

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

    df.drop(df[(df["cash_price"] == 'Not found')].index, inplace=True)

    df.to_csv('venex.csv')

    engine = create_engine_mysql()
"""    
    try:
        df.to_sql("products", con=engine, if_exists='append', index=False)
        print("Datos insertados en la base de datos.")
    except Exception as e:
        print("Error:", e)
"""
