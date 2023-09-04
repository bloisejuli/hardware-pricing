import requests
import lxml.html.soupparser as sp
from typing import List
from lxml.html import HtmlElement
import os
import datetime
import pandas as pd

def get_page_from_url(url: str) -> str:
    """
    Realiza una solicitud HTTP GET a la URL especificada y devuelve el contenido de la página.
    
    Args:
        url (str): La URL de la página a solicitar.
        
    Returns:
        str: El contenido de la página en formato de texto.
    """
    session = requests.Session()
    headers = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                    'Chrome/44.0.2403.157 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    response = session.get(url, headers=headers)
    data = response.content.decode('utf-8', 'replace')
    
    # Cierre de la sesión
    session.close()
    
    return data

def get_page_parsed(url: str) -> HtmlElement:
    """
    Realiza la solicitud HTTP GET a la URL especificada y devuelve la página analizada en forma de objeto lxml.
    
    Args:
        url (str): La URL de la página a analizar.
        
    Returns:
        lxml.html.HtmlElement: El objeto lxml que representa la página analizada.
    """
    page = get_page_from_url(url)
    parsed_page = sp.fromstring(page)
    return parsed_page

def get_text_or_not_found(elements: List[HtmlElement]) -> str:
    """
    Obtiene el texto del primer elemento de una lista de elementos lxml o devuelve "Not found" si la lista está vacía.
    
    Args:
        elements (List[HtmlElement]): Lista de elementos lxml.
        
    Returns:
        str: Texto del primer elemento o "Not found".
    """
    if elements:
        return elements[0].text
    else:
        return "Not found"

def extract_text_element(product: HtmlElement, xpath: str) -> str:
    """
    Extrae el texto de un elemento lxml utilizando una expresión XPath y devuelve "Not available" si no se encuentra.
    
    Args:
        product (lxml.html.HtmlElement): El elemento lxml del que se extraerá el texto.
        xpath (str): Expresión XPath para ubicar el elemento deseado.
        
    Returns:
        str: Texto del elemento o "Not available".
    """
    elements = product.xpath(xpath)
    if elements:
        return elements[0].strip()
    else:
        return "Not available"

def create_folder(folder_name: str) -> None:
    """
    Crea una carpeta si no existe en la ruta especificada.
    
    Args:
        folder_name (str): Nombre de la carpeta a crear.
        
    Returns:
        None
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f'Carpeta {folder_name} creada.')

def save_dataframes_to_csv(df: pd.DataFrame, df_notebooks: pd.DataFrame, page: str) -> None:
    """
    Guarda los DataFrames en archivos CSV en una carpeta con la fecha actual y el nombre de la página.
    
    Args:
        df (pd.DataFrame): DataFrame principal a guardar en CSV.
        df_notebooks (pd.DataFrame): DataFrame de notebooks a guardar en CSV.
        page (str): Nombre de la página para incluir en el nombre de archivo.
        
    Returns:
        None
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    folder_name = f'data/{current_date}'
    create_folder(folder_name)

    csv_filename = f'{folder_name}/{page}-{current_date}.csv'
    notebooks_csv_filename = f'{folder_name}/{page}-notebooks-{current_date}.csv'

    df.to_csv(csv_filename, index=False)
    df_notebooks.to_csv(notebooks_csv_filename, index=False)