
from PIL import Image
import base64
import io

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        # Leer el contenido de la imagen
        image_content = image_file.read()
        
        # Convertir la imagen a base64
        base64_image = base64.b64encode(image_content).decode("utf-8")
        
        return base64_image

# Ruta de la imagen a convertir
image_path = "C:/Users/varel/Pictures/T.png"

# Convertir la imagen a base64
base64_image = image_to_base64(image_path)

# Imprimir el resultado
print(len(base64_image))

def base64_to_image(base64_string):
    # Decodificar la cadena base64 a bytes
    image_bytes = base64.b64decode(base64_string)
    
    # Convertir los bytes a un objeto de imagen
    image = Image.open(io.BytesIO(image_bytes))
    
    # Mostrar la imagen
    image.show()

# Cadena base64 de la imagen

# Convertir la cadena base64 a imagen y mostrarla
#base64_to_image(base64_image)

import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('C:/Users/varel/Documents/ProjectDjango/quiniela/db.sqlite3')

# Crear un cursor
cursor = conn.cursor()

# Ejecutar la actualización
cursor.execute("UPDATE llenar_quiniela_imagenes_cartas SET T = '"+ base64_image +"';")

# Confirmar la transacción
conn.commit()

# Cerrar la conexión
conn.close()