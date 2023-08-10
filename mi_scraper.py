from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support.ui import Select

options = Options()
options.add_argument('--headless') # sin interfaz grafica
options.add_argument('--no-sandbox') # Seguridad
# options.add_argument('--disable-dev-shm-usage') # configuracion de linux
options.add_argument('--disable-gpu')
options.add_argument('--user-agent=""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36""') # user agent

wd = webdriver.Chrome(service=Service(), options=options)

url = "https://www.maximus.com.ar/"
wd.get(url)

# Ejecuto codigo de javacript para ir al final de la pagina
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 

# # Espero a que cargue la pagina
WebDriverWait(driver, timeout=5)


# El metodo Select nos permite acceder a las opciones en un menu desplegable (drop-down)
select = Select(driver.find_element(By.CLASS_NAME, 'menu-categorias menu-categorias-active'))
print (select)
print type(select)


#for item in select.options:
#    print(item.get_attribute('innerText'), item.get_attribute('value')) 
#    idzonapastorale_value.append(item.get_attribute('value'))
#    idzonapastorale_text.append(item.get_attribute('innerText'))




categories_xpath = "//div[contains(@class,'menu-categorias')]/ul[@class='categorias']/li[contains(@class,'menu-productos')]"
categories = wd.find_element(By.XPATH,categories_xpath)
print (size(categories))


