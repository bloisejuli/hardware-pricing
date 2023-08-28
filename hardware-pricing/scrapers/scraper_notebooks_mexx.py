from utils.web_utils import get_page_parsed
import re
import pandas

def extract_data(product):
    brand = product.xpath("//div[@itemprop='brand']/meta/@content")[0]
    model = product.xpath("//p[@class='mb-0']/b[contains(text(),'Modelo')]/../text()")[0].strip()
    processor = re.sub(r'\s*\(.*?\)', '', product.xpath("//p[@class='mb-0']/b[contains(text(),'Procesador')]/../text()")[0]).strip()
    memory = product.xpath("//p[@class='mb-0']/b[contains(text(),'Memoria')]/../text()")[0].strip()
    storage = product.xpath("//p[@class='mb-0']/b[contains(text(),'Almacenamiento')]/../text()")[0].strip()

    return{
        "brand":brand,
        "model":model,
        "processor":processor,
        "memory":memory,
        "storage":storage
    }


def extract_data_from_notebooks(df):

    data_list = []
    for index,row in df.iterrows():
        link = row['link']
        product = get_page_parsed(link)

        data = extract_data(product)
        data_list.append(data)

    df_notebooks = pandas.DataFrame.from_records(data_list)
    df_merged = pandas.concat([df, df_notebooks], axis=1)
    return df_merged