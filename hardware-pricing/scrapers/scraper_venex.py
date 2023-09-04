import pandas as pd
import datetime
from utils.web_utils import get_text_or_not_found, get_page_parsed, save_dataframes_to_csv
from scraper_notebooks_venex import extract_data_from_notebooks
from typing import List, Dict, Union
from lxml.html import HtmlElement

def extract_data(item: HtmlElement, category: str) -> Dict[str, Union[str, None]]:
    """
    Extrae información de un elemento de producto y la categoría a la que pertenece.
    
    Args:
        item (HtmlElement): Elemento HTML del producto.
        category (str): Categoría del producto.
        
    Returns:
        Dict[str, Union[str, None]]: Diccionario con información extraída del producto.
    """
    title = get_text_or_not_found(item.xpath(".//h3/a"))
    link = item.xpath(".//h3/a/@href")[0] if item.xpath(".//h3/a/@href") else None

    price_elements = item.xpath(".//span[@class='current-price']")
    cash_price = get_text_or_not_found(price_elements)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "category": category,
        "title": title.title(),
        "cash_price": cash_price,
        "link": link,
        "created_at": current_date
    }

def extract_data_from_categories(data_list: List[Dict[str, Union[str, None]]], categories: List[str], url: str) -> None:
    """
    Extrae información de productos de diferentes categorías y agrega los datos a la lista.
    
    Args:
        data_list (List[Dict[str, Union[str, None]]]): Lista para almacenar los datos extraídos.
        categories (List[str]): Lista de categorías de productos.
        url (str): URL base para construir las URLs de categoría.
    """
    for category in categories:
        page = get_page_parsed(f'{url}/{category}?limit=96')
        items = page.xpath("//div[contains(@class,'product')]/div/div")
        
        if category == 'precios-explosivos':
            category = 'outlet'
        
        for item in items:
            data = extract_data(item, category)
            data_list.append(data)

def preprocess_df_venex(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza el preprocesamiento del DataFrame de Venex.
    
    Args:
        df (pd.DataFrame): DataFrame a preprocesar.
        
    Returns:
        pd.DataFrame: DataFrame preprocesado.
    """
    df.drop(df[(df["cash_price"] == 'Not found')].index, inplace=True)
    df['cash_price'] = df['cash_price'].str.replace('[^0-9.]', '', regex=True).astype(float)

    df['store'] = 'venex'
    new_order = ['category', 'title', 'cash_price', 'store', 'link', 'created_at']
    df = df[new_order]
    return df

def main() -> None:
    """
    Función principal del script.
    """
    url = "https://www.venex.com.ar/"
    categories = ['notebooks', 'monitores', 'precios-explosivos']
    components = ['placas-de-video', 'memorias-ram']

    data_list = []

    extract_data_from_categories(data_list, categories, url)
    extract_data_from_categories(data_list, components, url + '/componentes-de-pc')
    df = pd.DataFrame.from_records(data_list)
    df_venex = preprocess_df_venex(df)
    print(df_venex)

    df_notebooks = extract_data_from_notebooks(df_venex[df_venex['category'] == 'notebooks'])
    print(df_notebooks)

    save_dataframes_to_csv(df_venex, df_notebooks, 'venex')

if __name__ == '__main__':
    main()
