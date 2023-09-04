import pandas as pd
import datetime
from utils.web_utils import get_page_parsed, get_text_or_not_found, save_dataframes_to_csv
from scraper_notebooks_mexx import extract_data_from_notebooks
from typing import List, Dict
from lxml.html import HtmlElement

def extract_data(item: HtmlElement, category: str) -> Dict[str, str]:
    """
    Extrae información de un elemento de producto.

    Args:
        item (Any): Elemento HTML del producto.
        category (str): Categoría del producto.

    Returns:
        Dict[str, str]: Diccionario con la información extraída.
    """
    title = get_text_or_not_found(item.xpath(".//h4/a"))
    link = item.xpath("div/div[contains(@class,'overlay')]/a/@href")[0]
    price_elements = item.xpath(".//div[contains(@class, 'price')]/h4/b")
    cash_price = get_text_or_not_found(price_elements)

    return {
        "category": category,
        "title": title,
        "cash_price": cash_price,
        "link": link
    }

def get_mexx_data(categories: List[str]) -> pd.DataFrame:
    """
    Obtiene datos de productos de la tienda Mexx.

    Args:
        categories (List[str]): Lista de categorías de productos.

    Returns:
        pd.DataFrame: DataFrame con los datos de productos.
    """
    data_list = []

    for category in categories:
        page = get_page_parsed(f'https://www.mexx.com.ar/productos-rubro/{category}/?all=1')
        items = page.xpath("//div[contains(@class,'productos')]")
        for item in items:
            data = extract_data(item, category)
            data_list.append(data)

    df = pd.DataFrame.from_records(data_list)
    return df

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y transforma el DataFrame de productos.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.

    Returns:
        pd.DataFrame: DataFrame limpio y transformado.
    """
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.drop(df[(df["cash_price"] == 'Not found')].index, inplace=True)
    df.drop(df[(df["title"] == 'Not found')].index, inplace=True)
    df['cash_price'] = df['cash_price'].str.replace('.', '', regex=False)
    df['cash_price'] = df['cash_price'].str.replace(',', '.', regex=False)
    df['cash_price'] = df['cash_price'].str.replace('[^0-9.]', '', regex=True).astype(float)
    df['title'] = df['title'].str.rstrip('#')
    df['store'] = 'mexx'
    df['created_at'] = created_at
    new_order = ['category', 'title', 'cash_price', 'store', 'link', 'created_at']
    df = df[new_order]

    return df

def main() -> None:
    """
    Función principal del script.
    """
    categories = ['notebooks', 'memorias-ram', 'placas-de-video', 'monitores', 'outlet']

    df = get_mexx_data(categories)
    df_cleaned = clean_df(df)

    print(df_cleaned)

    df_notebooks = extract_data_from_notebooks(df_cleaned[df_cleaned['category'] == 'notebooks'])
    print(df_notebooks)

    save_dataframes_to_csv(df, df_notebooks, 'mexx')

if __name__ == '__main__':
    main()
