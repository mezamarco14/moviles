import csv
import json

# Ruta del archivo CSV
csv_file = r"C:\Users\HP\Desktop\coscmo\data mejorada.csv"  # Ruta del archivo CSV
json_file = r"C:\Users\HP\Desktop\coscmo\datos.json"  # Ruta de salida del archivo JSON

# Convertir CSV a JSON
data = []
with open(csv_file, encoding='utf-8-sig') as csvfile:
    # Usamos el delimitador correcto ';' para leer el archivo CSV
    reader = csv.DictReader(csvfile, delimiter=';')

    # Imprimir los encabezados para asegurarnos de que se leen correctamente
    print(reader.fieldnames)  # Esto te mostrará los nombres de las columnas

    for row in reader:
        # Crear un diccionario con los datos que se deben guardar
        record = {
            "Ciclo": row["Ciclo"],  # Columna "Ciclo"
            "Escuela": row["Escuela"],  # Columna "Escuela"
            "Facultad": row["Facultad"],  # Columna "Facultad"
            "Genero": row["Genero"],  # Columna "Genero"
            "Peso": row["Peso"],  # Columna "Peso"
            "Altura": row["Altura"],  # Columna "Altura"
            "Intervencion": row["Intervencion"],  # Columna "Intervencion"
            "Fecha": row["Fecha"]  # Columna "Fecha"
        }
        data.append(record)

# Guardar el JSON
with open(json_file, "w", encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=4)

print("Conversión completada.")
