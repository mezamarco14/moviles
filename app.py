from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import csv
import json
from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Cosmos DB desde las variables de entorno
url = os.getenv("COSMOS_DB_URL")  # No necesitas cambiar esto
key = os.getenv("COSMOS_DB_KEY")  # No necesitas cambiar esto
database_name = os.getenv("COSMOS_DB_DATABASE_NAME")  # Cambié el nombre
container_name = os.getenv("COSMOS_DB_CONTAINER_NAME")  # Cambié el nombre

# Validar que las variables de entorno están presentes
if not all([url, key, database_name, container_name]):
    raise ValueError("Faltan variables de entorno esenciales para Cosmos DB.")

# Configuración de Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Crear cliente de Cosmos DB
client = CosmosClient(url, credential=key)

# Intentar obtener la base de datos y contenedor, manejar errores de conexión
try:
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
except exceptions.CosmosResourceNotFoundError as e:
    print(f"Error al encontrar la base de datos o el contenedor: {e}")
    raise
except exceptions.CosmosClientError as e:
    print(f"Error de cliente Cosmos DB: {e}")
    raise

# Verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Convertir CSV a JSON
def csv_to_json(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')  # Usamos el delimitador ';' para CSV
        for row in reader:
            record = {
                "Ciclo": row["Ciclo"],
                "Escuela": row["Escuela"],
                "Facultad": row["Facultad"],
                "Genero": row["Genero"],
                "Peso": row["Peso"],
                "Altura": row["Altura"],
                "Intervencion": row["Intervencion"],
                "Fecha": row["Fecha"]
            }
            data.append(record)
    return data

# Subir el archivo CSV
@app.route('/')
def index():
    return render_template('index.html')

# Procesar el archivo cargado
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No se encontró el archivo en la solicitud.")  # Depuración
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        print("El archivo no tiene nombre.")  # Depuración
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Verificar si el directorio de carga existe, si no, crearlo
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        file.save(file_path)

        # Validar el contenido del archivo CSV
        try:
            data = csv_to_json(file_path)
        except Exception as e:
            print(f"Error al convertir el archivo CSV: {e}")
            return 'Error al procesar el archivo CSV'
        
        # Subir los datos a Cosmos DB
        for record in data:
            try:
                # Verificar si el registro ya existe en Cosmos DB
                record["id"] = f"{record['Ciclo']}-{record['Escuela']}-{record['Fecha']}"
                container.upsert_item(record)
            except exceptions.CosmosResourceExistsError as e:
                print(f"El registro ya existe en Cosmos DB: {e}")
            except Exception as e:
                print(f"Error al insertar el registro: {record}")
                print(e)
        
        return f"¡Datos cargados exitosamente a Cosmos DB!"

    print("Archivo no válido.")  # Depuración
    return 'Archivo no válido'

# Verificar si el archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)
