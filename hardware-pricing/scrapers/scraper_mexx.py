import pandas
from database_connector.my_sql_connector import create_engine_mysql
from utils.web_utils import get_text_or_not_found, get_page_parsed
from scraper_notebooks_mexx import extract_data_from_notebooks
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
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    df['cash_price'] = df['cash_price'].str.replace('.', '', regex=False)
    df['cash_price'] = df['cash_price'].str.replace(',', '.', regex=False)
    df['cash_price'] = df['cash_price'].str.replace('[^0-9.]', '', regex=True).astype(float)
    df['store'] = 'mexx'
    new_order = ['category', 'title', 'cash_price', 'store', 'link', 'created_at']
    df = df[new_order]
    print(df)
    df.to_csv(f'../data/mexx-{current_date}.csv')

    df_notebooks = extract_data_from_notebooks(df[df['category'] == 'notebooks'])

    new_column_order = [col for col in df_notebooks.columns if col != 'created_at'] + ['created_at']
    df_notebooks = df_notebooks[new_column_order]

    df_notebooks.to_csv(f'../data/mexx-notebooks-{current_date}.csv')

    engine = create_engine_mysql()

    try:
        df.to_sql("products", con=engine, if_exists='append', index=False)
        print("Datos insertados en la base de datos.")
    except Exception as e:
        print("Error:", e)


    

