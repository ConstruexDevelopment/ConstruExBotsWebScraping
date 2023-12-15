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

        # Filtrar el texto que contiene "Calle" o "Avenida"
        texto_filtrado = [parrafo.text.strip() for parrafo in soup.find_all('p') if 'Calle' in parrafo.text or 'Avenida' in parrafo.text]

        # Extraer y guardar las direcciones en un archivo CSV
        if texto_filtrado:
            with open('direcciones.csv', 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID_exhibidor', 'Enlace', 'Texto']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                for texto in texto_filtrado:
                    writer.writerow({'ID_exhibidor': id_exhibidor, 'Enlace': link, 'Texto': texto})
        else:
            # Si no hay texto filtrado, guardar en un archivo diferente
            with open('sin_texto.csv', 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID_exhibidor', 'Enlace']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'ID_exhibidor': id_exhibidor, 'Enlace': link})

    except requests.exceptions.RequestException as e:
        print(f"Error en {link}: {str(e)}")
    except Exception as e:
        print(f"Error general en {link}: {str(e)}")

# Leer enlaces desde un archivo CSV latin-1
with open('enlaces.csv', 'r', newline='', encoding='utf-8') as enlaces_file:
    reader = csv.DictReader(enlaces_file, delimiter=';')
    enlaces = [(row.get('ID_exhibidor', ''), row.get('Enlace', '')) for row in reader]

# Crear o truncar los archivos CSV antes de comenzar
with open('direcciones.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['ID_exhibidor', 'Enlace', 'Texto']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

with open('sin_texto.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['ID_exhibidor', 'Enlace']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# Iterar sobre cada enlace y extraer direcciones
for id_exhibidor, enlace in enlaces:
    extraer_direccion(enlace, id_exhibidor)
