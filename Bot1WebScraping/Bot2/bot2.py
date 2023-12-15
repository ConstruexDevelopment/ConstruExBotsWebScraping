import csv
import requests
from bs4 import BeautifulSoup

def extraer_contenido(link):
    try:
        # Realizar la solicitud HTTP
        response = requests.get(link)
        response.raise_for_status()  # Lanza una excepción para errores HTTP

        # Analizar el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Clases a buscar
        clases = ['subtitulo', 'textito', 'companyname', 'e-mail']

        # Extraer y guardar el contenido de las clases en un archivo CSV
        with open('contenido_html.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Enlace', 'Clase', 'Contenido']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for clase in clases:
                elementos = soup.find_all(class_=clase)
                if elementos:
                    for elemento in elementos:
                        writer.writerow({'Enlace': link, 'Clase': clase, 'Contenido': str(elemento)})
    except Exception as e:
        print(f"Error en {link}: {str(e)}")

# Leer enlaces desde un archivo CSV
with open('enlaces.csv', 'r', newline='', encoding='utf-8') as enlaces_file:
    reader = csv.DictReader(enlaces_file)
    enlaces = [row['Enlace'] for row in reader]

# Crear o truncar el archivo CSV antes de comenzar
with open('contenido_html.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Enlace', 'Clase', 'Contenido']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# Iterar sobre cada enlace y extraer contenido de las clases
for enlace in enlaces:
    extraer_contenido(enlace)
