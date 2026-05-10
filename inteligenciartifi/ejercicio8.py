import ollama

pedido = input("¿Qué consulta SQL quieres generar? ")

prompt = f"""
Genera una consulta SQL para PostgreSQL según esta solicitud:
{pedido}
Devuelve solo SQL válido sin explicaciones.
"""

respuesta = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': prompt}]
)

sql_generado = respuesta['message']['content']

with open("script.sql", "w", encoding="utf-8") as archivo:
    archivo.write(sql_generado)

print("Consulta guardada en script.sql")
print(sql_generado)