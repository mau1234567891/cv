import ollama
import pandas as pd
from io import StringIO

# Pedir datos
tema = input("¿Qué tabla quieres crear? ")
filas = input("¿Cuántas filas deseas generar? ")

# Prompt para la IA
prompt = f"""
Genera una tabla CSV sobre {tema} con {filas} filas.
Solo devuelve CSV válido, sin explicaciones.
"""

respuesta = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': prompt}]
)

csv_texto = respuesta['message']['content']

# Convertir CSV a DataFrame
df = pd.read_csv(StringIO(csv_texto))

# Crear nombre de archivo automático
nombre_archivo = tema.replace(" ", "_") + ".xlsx"

# Guardar Excel
df.to_excel(nombre_archivo, index=False)

print(f"Archivo creado correctamente: {nombre_archivo}")
print(df)