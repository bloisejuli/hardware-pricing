import pandas as pd
from utils.web_utils import get_page_parsed
from lxml.html import HtmlElement
from typing import List, Dict, Union

def extract_brand(words: List[str]) -> str:
    """
    Extrae la marca de un producto de una lista de palabras.
    
    Args:
        words (List[str]): Lista de palabras en el título del producto.
        
    Returns:
        str: Marca del producto.
    """
    try:
        notebook_index = words.index("Notebook")
        brand = words[notebook_index + 1]
    except:
        brand = words[0]
    return brand

def extract_model(product: HtmlElement) -> str:
    """
    Extrae el modelo de un producto a partir de su elemento HTML.
    
    Args:
        product (HtmlElement): Elemento HTML del producto.
        
    Returns:
        str: Modelo del producto.
    """
    try:
        words = product.xpath("//*[@id='cart_quantity']/div[2]/p")[0].text.split()
        model = words[1]
    except:
        model = "Not Found"
    return model

def extract_features(product: HtmlElement) -> Dict[str, str]:
    """
    Extrae las características de un producto a partir de su elemento HTML.
    
    Args:
        product (HtmlElement): Elemento HTML del producto.
        
    Returns:
        Dict[str, str]: Diccionario de características del producto.
    """
    elements = product.xpath("//div[contains(@class, 'features-content')]//div[@class = 'option-info hidden-xs']")
    if not elements:
        return {}

    list_features = {}
    for element in elements:
        feature_title = element.xpath(".//div[@class='option-title']")[0].text
        feature = element.xpath(".//div[@class='option-content']")[0].text
        list_features[feature_title] = feature
    return list_features

def extract_processor(list_features: Dict[str, str]) -> str:
    """
    Extrae el procesador de un producto a partir de su diccionario de características.
    
    Args:
        list_features (Dict[str, str]): Diccionario de características del producto.
        
    Returns:
        str: Información del procesador del producto.
    """
    marca_key = next((key for key in list_features.keys() if key in ["Intel:", "AMD:"]), None)
    marca = "Intel" if marca_key == "Intel:" else "AMD"
    procesador_marca = list_features.get(marca_key)
    procesador_modelo = list_features.get("Modelo:")
    processor = f'{marca} {procesador_marca} {procesador_modelo}'
    return processor

def extract_data_notebook(product: HtmlElement, words: List[str]) -> Dict[str, Union[str, None]]:
    """
    Extrae información detallada de una notebook a partir de su elemento HTML y lista de palabras en el título.
    
    Args:
        product (HtmlElement): Elemento HTML del producto.
        words (List[str]): Lista de palabras en el título del producto.
        
    Returns:
        Dict[str, Union[str, None]]: Diccionario con información detallada de la notebook.
    """
    brand = extract_brand(words)
    model = extract_model(product)
    list_features = extract_features(product)
    processor = extract_processor(list_features)

    return {
        "brand": brand.title(),
        "model": model,
        "processor": processor,
        "memory": list_features.get("Capacidad:"),
        "storage": list_features.get("Disco Sólido:") or list_features.get("Capacidad:")
    }

def extract_data_from_notebooks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae información detallada de notebooks y fusiona los DataFrames resultantes.
    
    Args:
        df (pd.DataFrame): DataFrame con la información de productos.
        
    Returns:
        pd.DataFrame: DataFrame fusionado y limpio.
    """
    data_list = []
    for index,row in df.iterrows():
        link = row['link']
        product = get_page_parsed(link)
        words = row['title'].split()    
        data = extract_data_notebook(product, words)
        data_list.append(data)

    df_notebooks = pd.DataFrame.from_records(data_list)
    df_merged = pd.concat([df, df_notebooks], axis=1)
    new_order = ['category', 'title', 'cash_price', 'store', 'link', 'brand', 'model', 'processor', 'memory', 'storage', 'created_at']
    df_merged = df_merged[new_order]
    df_merged.drop(df_merged[df_merged['model'] == 'Not Found'].index, inplace=True)
    df_merged.dropna(inplace=True)

    return df_merged
