import subprocess
import time

# Marca de tiempo de inicio
inicio_tiempo = time.time()

# Ruta de los scripts que deseas ejecutar
ruta_script1 = 'scrapers/scraper_mexx.py'
ruta_script2 = 'scrapers/scraper_venex.py'

print("Ejecutando scraper_mexx..")
# Ejecuta script1.py
print(ruta_script1)
resultado_script1 = subprocess.run(['python3', ruta_script1], capture_output=True, text=True)

# Imprime la salida de script1.py
print("Salida de scraper_mexx.py:")
print(resultado_script1.stdout)

print("Ejecutando scraper_venex..")
# Ejecuta script2.py
resultado_script2 = subprocess.run(['python3', ruta_script2], capture_output=True, text=True)

# Imprime la salida de script2.py
print("Salida de scraper_venex.py:")
print(resultado_script2.stdout)


# Marca de tiempo de finalización
fin_tiempo = time.time()

# Calcula el tiempo transcurrido
tiempo_transcurrido = (fin_tiempo - inicio_tiempo)/60

# Muestra el tiempo transcurrido en segundos
print(f"Fin del programa, este tardó {tiempo_transcurrido:.2f} minutos en ejecutarse.")