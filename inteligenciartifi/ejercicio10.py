import ollama
import pandas as pd
from io import StringIO

def limpiar_respuesta_csv(texto):
    """Limpia etiquetas de markdown o texto extra que la IA pueda incluir."""
    texto_limpio = texto.replace("```csv", "").replace("```", "").strip()
    return texto_limpio

# 1. Configuración de parámetros
tema = input("¿Qué tabla quieres crear? ")
filas = input("¿Cuántas filas deseas generar? ")

# 2. Generación inicial
print(f"\n[1/3] Generando tabla original sobre: {tema}...")
prompt_creacion = f"""
Genera una tabla CSV sobre {tema} con {filas} filas.
Solo devuelve el contenido CSV, sin texto adicional ni bloques de código.
"""

respuesta = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': prompt_creacion}]
)

csv_texto = limpiar_respuesta_csv(respuesta['message']['content'])
df = pd.read_csv(StringIO(csv_texto))

print("\n--- Vista previa de la tabla creada ---")
print(df.head())

# 3. Modificación del mismo archivo
cambio = input("\n¿Qué modificación deseas aplicar? (ej: 'Suma 10 a la columna X', 'Traduce todo'): ")

# Extraemos las columnas para forzar a la IA a respetarlas
columnas_actuales = ", ".join(df.columns)
csv_actual = df.to_csv(index=False)

print(f"\n[2/3] Aplicando cambios...")
prompt_modificacion = f"""
Actúa como un editor de datos profesional. 
Tengo el siguiente CSV:
{csv_actual}

Tarea: {cambio}

REGLAS ESTRICTAS:
1. Mantén exactamente estos nombres de columnas: {columnas_actuales}.
2. No inventes columnas nuevas a menos que la tarea lo pida.
3. Devuelve ÚNICAMENTE el código CSV resultante. Sin explicaciones.
"""

respuesta_mod = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': prompt_modificacion}]
)

csv_modificado = limpiar_respuesta_csv(respuesta_mod['message']['content'])

# Intentamos cargar la modificación
try:
    df_final = pd.read_csv(StringIO(csv_modificado))
    
    # 4. Guardar resultado final
    print(f"\n[3/3] Guardando archivo...")
    nombre_archivo = tema.replace(" ", "_") + ".xlsx"
    df_final.to_excel(nombre_archivo, index=False)

    print(f"\n✅ Proceso completado con éxito.")
    print(f"Archivo guardado como: {nombre_archivo}")
    print("\n--- Resultado Final ---")
    print(df_final)

except Exception as e:
    print(f"\n❌ Error al procesar la modificación: {e}")
    print("La IA devolvió un formato no válido.")