import pandas
from my_sql_connector import create_engine_mysql
from web_utils import get_text_or_not_found, get_page_parsed
import datetime


def get_mexx_data(categories):
    data_list = []

    for category in categories:
        page = get_page_parsed(f'https://www.mexx.com.ar/productos-rubro/{category}/?all=1')
        items = page.xpath("//div[contains(@class,'productos')]")
        for item in items:
            data = extract_data(item, category)
            data_list.append(data)         

    df = pandas.DataFrame.from_records(data_list)
    return df

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
    categories = ['notebooks', 'memorias-ram','placas-de-video','monitores','outlet']
    data_list = []

    df = get_mexx_data(categories)
    df.to_csv('mexx.csv')

    engine = create_engine_mysql()

    try:
        df.to_sql("products", con=engine, if_exists='append', index=False)
        print("Datos insertados en la base de datos.")
    except Exception as e:
        print("Error:", e)
