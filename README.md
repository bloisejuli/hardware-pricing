# Hardware Pricing

## Instalación

### Requisitos previos
Asegúrate de tener instalado Python3 en tu sistema.

### Creación de entorno virtual
Se recomienda crear un entorno virtual para trabajar con Python. Puedes hacerlo de la siguiente manera:

1. Crea el entorno virtual:
python3 -m venv nombre-del-entorno

2. Activa el entorno virtual:
source nombre-del-entorno/bin/activate


3. Para desactivar el entorno virtual cuando hayas terminado:
deactivate


### Instalación de dependencias
Para instalar todas las bibliotecas que utilizamos, ejecuta el siguiente comando:
pip install -r requirements.txt

## Uso
Los datos se almacenan en una base de datos en la tabla "products", pero tambien creamos un csv de cada pagina.
Escrapeamos dos paginas y para ambas nos encargamos de traer los datos para las categorias:
- notebooks
- memorias-ram
- placas-de-video
- monitores
- outlet

## Archivos
* scraper_mexx.py: Se encarga de obtener los datos de la pagina https://www.mexx.com.ar/
* scraper_venex.py: Se encarga de obtener los datos de la pagina https://www.venex.com.ar/
* my_sql_connector.py: Se encarga de la crear la conexion con la base de datos
* web_utils.py: Contiene las funciones que utilizamos para facilitar la obtención, el procesamiento y la extracción de información de páginas web.
