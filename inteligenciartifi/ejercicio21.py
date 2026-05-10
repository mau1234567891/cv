import ollama
import os

def analizar_archivo_sospechoso():
    print("\n--- [ AGENTE DE CIBERSEGURIDAD: SCANNER ] ---")
    
    # 1. Pedir el nombre del archivo
    nombre_archivo = input("Introduce el nombre del archivo a analizar (ej. correo.txt): ")

    # Verificar si el archivo existe
    if not os.path.exists(nombre_archivo):
        print(f"❌ Error: El archivo '{nombre_archivo}' no existe en esta carpeta.")
        return

    try:
        # 2. Leer el contenido del archivo
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()

        print(f"🔍 Escaneando patrones en '{nombre_archivo}'...")

        # 3. Llama 3 busca patrones sospechosos
        prompt_seguridad = f"""
        Analiza el siguiente texto extraído de un archivo. 
        Busca patrones de:
        - Phishing (suplantación de identidad).
        - Enlaces maliciosos o dominios falsos.
        - Lenguaje de manipulación psicológica (urgencia, miedo).
        - Solicitudes inusuales de datos sensibles.

        TEXTO A ANALIZAR:
        \"\"\"{contenido}\"\"\"

        RESPUESTA:
        1. Nivel de Riesgo (Bajo, Medio, Alto).
        2. Lista de patrones sospechosos encontrados.
        3. Recomendación final.
        """

        respuesta = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt_seguridad}]
        )

        # 4. Resultado
        print("\n" + "🛡️" * 15)
        print(f"REPORTE DE SEGURIDAD PARA: {nombre_archivo}")
        print(respuesta['message']['content'])
        print("🛡️" * 15)

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    analizar_archivo_sospechoso()