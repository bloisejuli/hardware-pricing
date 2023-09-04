import pandas as pd
import re
from utils.web_utils import get_page_parsed, extract_text_element
from typing import Any, Dict, List
from lxml.html import HtmlElement

def extract_data_notebook(product: HtmlElement) -> Dict[str, str]:
    """
    Extrae información sobre una notebook a partir del elemento HTML del producto.
    
    Args:
        product (Any): Elemento HTML del producto.
        
    Returns:
        Dict[str, str]: Un diccionario con la información extraída.
    """
    brand = product.xpath("//div[@itemprop='brand']/meta/@content")[0]
    model = extract_text_element(product, "//p[@class='mb-0']/b[contains(text(),'Modelo')]/../text()")
    processor = extract_text_element(product, "//p[@class='mb-0']/b[contains(text(),'Procesador')]/../text()")
    processor = re.sub(r'\s*\(.*?\)', '', processor).strip()
    memory = extract_text_element(product, "//p[@class='mb-0']/b[contains(text(),'Memoria')]/../text()")
    storage = extract_text_element(product, "//p[@class='mb-0']/b[contains(text(),'Almacenamiento')]/../text()")

    return{
        "brand":brand.title(),
        "model":model,
        "processor":processor,
        "memory":memory,
        "storage":storage
    }

def clean_df_notebooks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el DataFrame eliminando filas con valores 'Not available'.
    
    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        
    Returns:
        pd.DataFrame: DataFrame limpio.
    """
    columns_to_check = ['model', 'processor', 'memory', 'storage']
    for column in columns_to_check:
        df.drop(df[df[column] == 'Not available'].index, inplace=True)
    return df

def extract_data_from_notebooks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae información de notebooks y fusiona los DataFrames resultantes.
    
    Args:
        df (pd.DataFrame): DataFrame con la información de productos.
        
    Returns:
        pd.DataFrame: DataFrame fusionado y limpio.
    """
    data_list: List[Dict[str, str]] = []
    for index, row in df.iterrows():
        link = row['link']
        product = get_page_parsed(link)

        data = extract_data_notebook(product)
        data_list.append(data)
    
    df_notebooks = pd.DataFrame.from_records(data_list)
    df_notebooks = clean_df_notebooks(df_notebooks)
    
    df_merged = pd.concat([df, df_notebooks], axis=1)
    new_order = ['category', 'title', 'cash_price', 'store', 'link', 'brand', 'model', 'processor', 'memory', 'storage', 'created_at']
    df_merged = df_merged[new_order]
    df_merged.dropna(inplace=True)
    return df_merged
