import requests
import lxml.html.soupparser as sp

def get_page_from_url(url: str):
    session = requests.Session()
    response = session.get(url, headers={
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                    'Chrome/44.0.2403.157 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    })

    data = response.content.decode('utf-8')
    return data


def get_page_parsed(url: str):
    page = get_page_from_url(url)
    parsed_page = ''
    parsed_page = sp.fromstring(page)
    return parsed_page


def get_text_or_not_found(elements):
    if elements:
        return elements[0].text
    else:
        return "Not found"

def extract_data(item):
    discount_applied = get_text_or_not_found(item.xpath("span"))
    product = get_text_or_not_found(item.xpath(".//h4/a"))
    link = item.xpath("div/div[contains(@class,'overlay')]/a/@href")[0]
    price_elements = item.xpath(".//div[contains(@class, 'price')]/h4/b")
    price = get_text_or_not_found(price_elements)

    return {
        "Discount": discount_applied,
        "Product": product,
        "Price": price,
        "Link": link
    }

def print_data(data_list):
    for item_data in data_list:
        print("Discount:", item_data["Discount"])
        print("Product:", item_data["Product"])
        print("Price:", item_data["Price"])
        print("Link:", item_data["Link"])
        print("-" * 20)



page = get_page_parsed("https://www.mexx.com.ar/productos-rubro/notebooks/?all=1")
items = page.xpath("//div[contains(@class,'listado-1 listados')]/div[contains(@class,'productos')]")

data_list = []

for item in items:
    data = extract_data(item)
    data_list.append(data)

print_data(data_list)


