import pandas
from utils.web_utils import get_page_parsed, get_text_or_not_found

def extract_data(product, words):
    try:
        notebook_index = words.index("Notebook")
        brand = words[notebook_index + 1]
    except:
        brand = words[0]

        
    try:
        words = product.xpath("//*[@id='cart_quantity']/div[2]/p")[0].text.split()
        model = words[1]
    except:
        model = "Not Found"

    elements = product.xpath("//div[contains(@class, 'features-content')]//div[@class = 'option-info hidden-xs']")
    
    if not elements:
        return {}

    list_features = {}
    for element in elements:
        feature_title = element.xpath(".//div[@class='option-title']")[0].text
        feature = element.xpath(".//div[@class='option-content']")[0].text
        list_features[feature_title] = feature

    try:
        procesador_marca = list_features.get("Intel:")
        marca = "Intel"
    except:
        procesador_marca = list_features.get("AMD:")
        marca = "AMD"
    
    procesador_modelo = list_features.get("Modelo:")
    processor = f'{marca} {procesador_marca} {procesador_modelo}'

    return{
        "brand":brand,
        "model":model,
        "processor":processor,
        "memory":list_features["Capacidad:"],
        "storage":list_features.get("Disco S�lido:") or list_features.get("Capacidad:")
    }


def extract_data_from_notebooks(df):

    data_list = []
    for index,row in df.iterrows():
        link = row['link']
        product = get_page_parsed(link)
        words = row['title'].split()    
        data = extract_data(product, words)
        data_list.append(data)

    df_notebooks = pandas.DataFrame.from_records(data_list)
    df_merged = pandas.concat([df, df_notebooks], axis=1)
    cleaned_df = df_merged.dropna(subset=['brand', 'model'])
    return cleaned_df





