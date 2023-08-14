from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapper_categories import obtain_url_categories
url_categories = obtain_url_categories()
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"')

wd = webdriver.Chrome(options=options)
for url in url_categories:
    if 'Notebooks' in url:
        wd.get(url)
        WebDriverWait(wd, 10)
        print("HOLAAA")
        prices_xpath = '//div[@id="articulos"]//div[@class="product"]//div[@class="price"]'
        prices_elements = wd.find_elements(By.XPATH, prices_xpath)
        print(prices_elements)
        print(type(prices_elements))
        for price_element in prices_elements:
            price_text = price_element.text
            print(price_text)
            print("HOLA")
wd.quit()