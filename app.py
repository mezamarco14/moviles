from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import csv
import json
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Cosmos DB desde las variables de entorno
url = os.getenv("COSMOS_DB_URL")  # URL de tu cuenta de Cosmos DB
key = os.getenv("COSMOS_DB_KEY")  # Clave de acceso a Cosmos DB
database_name = os.getenv("COSMOS_DB_DATABASE")  # Nombre de la base de datos
container_name = os.getenv("COSMOS_DB_CONTAINER")  # Nombre del contenedor

# Configuración de Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Crear cliente de Cosmos DB
client = CosmosClient(url, credential=key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

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
        file.save(file_path)

        # Convertir el archivo CSV a JSON
        data = csv_to_json(file_path)

        # Subir los datos a Cosmos DB
        for record in data:
            try:
                record["id"] = f"{record['Ciclo']}-{record['Escuela']}-{record['Fecha']}"
                container.upsert_item(record)
            except Exception as e:
                print(f"Error al insertar el registro: {record}")
                print(e)
        
        return f"¡Datos cargados exitosamente a Cosmos DB!"

    print("Archivo no válido.")  # Depuración
    return 'Archivo no válido'

# Verificar si el archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)
