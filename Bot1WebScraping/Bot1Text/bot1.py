import csv
import requests
import chardet

from bs4 import BeautifulSoup

def extraer_direccion(link):
    try:
        # Realizar la solicitud HTTP
        response = requests.get(link)
        
        # Verificar el código de estado
        if response.status_code == 200:
            response.raise_for_status()  # Lanza una excepción para errores HTTP

            # Analizar el contenido HTML de la página
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontrar elementos con la clase "address" contenido
            direcciones = soup.find_all(class_='address')

            # Extraer y guardar las direcciones en un archivo CSV
            if direcciones:
                with open('direcciones.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Enlace', 'Dirección']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    for direccion in direcciones:
                        writer.writerow({'Enlace': link, 'Dirección': direccion.text.strip()})
        else:
            print(f"Error en {link}: {response.status_code}")
    except Exception as e:
        print(f"Error en {link}: {str(e)}")

# Leer enlaces desde un archivo CSV
with open('enlaces.csv', 'r', newline='', encoding='latin-1') as enlaces_file:
    reader = csv.DictReader(enlaces_file)
    enlaces = [row['Enlace'] for row in reader]

# Crear o truncar el archivo CSV antes de comenzar
with open('direcciones.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Enlace', 'Dirección']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# Iterar sobre cada enlace y extraer direcciones
for enlace in enlaces:
    extraer_direccion(enlace)
