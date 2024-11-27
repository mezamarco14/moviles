from azure.cosmos import CosmosClient
import json
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Cosmos DB desde las variables de entorno
url = os.getenv('COSMOS_DB_URL')  # URL de tu cuenta de Cosmos DB
key = os.getenv('COSMOS_DB_KEY')  # Clave de Cosmos DB
database_name = os.getenv('COSMOS_DB_DATABASE_NAME')  # Nombre de la base de datos
container_name = os.getenv('COSMOS_DB_CONTAINER_NAME')  # Nombre del contenedor

# Ruta del archivo JSON
json_file = r"C:\Users\HP\Desktop\coscmo\datos.json"  # Ruta de salida del archivo JSON

# Crear cliente de Cosmos DB
client = CosmosClient(url, credential=key)

# Obtener la base de datos y el contenedor
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Leer el archivo JSON
with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Insertar cada registro en el contenedor
for record in data:
    try:
        # Es importante tener un "id" único para cada registro en Cosmos DB
        record["id"] = f"{record['Ciclo']}-{record['Escuela']}-{record['Fecha']}"  # Genera un ID único
        container.upsert_item(record)  # Inserta o actualiza el ítem
        print(f"Registro insertado: {record}")
    except Exception as e:
        print(f"Error al insertar el registro: {record}")
        print(e)

print("Todos los registros se han subido a Cosmos DB.")
