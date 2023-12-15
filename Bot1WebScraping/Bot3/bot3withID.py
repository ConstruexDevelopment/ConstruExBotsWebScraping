import csv
import requests
from bs4 import BeautifulSoup

def extraer_direccion(link, id_exhibidor):
    try:
        # Verificar si la URL está presente
        link = link.strip()  # Eliminar espacios al principio y al final
        if not link:
            print(f"URL vacía para ID_exhibidor {id_exhibidor}")
            return

        # Realizar la solicitud HTTP
        print(f'Enlace para ID_exhibidor {id_exhibidor}: {link}')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(link, headers=headers)
        response.raise_for_status()

        # Analizar el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar elementos con la clase "address"
        direcciones = soup.find_all(class_='address')

        # Extraer y guardar las direcciones en un archivo CSV
        if direcciones:
            with open('direcciones.csv', 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID_exhibidor', 'Enlace', 'Dirección']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                for direccion in direcciones:
                    writer.writerow({'ID_exhibidor': id_exhibidor, 'Enlace': link, 'Dirección': direccion.text.strip()})

    except requests.exceptions.RequestException as e:
        print(f"Error en {link}: {str(e)}")
    except Exception as e:
        print(f"Error general en {link}: {str(e)}")

# Leer enlaces desde un archivo CSV latin-1
with open('enlaces.csv', 'r', newline='', encoding='utf-8') as enlaces_file:
    reader = csv.DictReader(enlaces_file, delimiter=';')
    enlaces = [(row.get('ID_exhibidor', ''), row.get('Enlace', '')) for row in reader]

# Crear o truncar el archivo CSV antes de comenzar
with open('direcciones.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['ID_exhibidor', 'Enlace', 'Dirección']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# Iterar sobre cada enlace y extraer direcciones
for id_exhibidor, enlace in enlaces:
    #print(f'ID_exhibidor: {id_exhibidor}, Enlace: {enlace}')
    extraer_direccion(enlace, id_exhibidor)
