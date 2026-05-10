import ollama
import os
import time

# Configuración de rutas
ESCRITORIO = os.path.join(os.path.expanduser("~"), "Desktop")
CARPETA_PROYECTOS = os.path.join(ESCRITORIO, "IA_Generados")

# Asegurarnos de que la carpeta base exista
if not os.path.exists(CARPETA_PROYECTOS):
    os.makedirs(CARPETA_PROYECTOS)

def ia_crear_archivos(instruccion):
    print(f"📂 Procesando solicitud: {instruccion}")
    
    # Prompt para que la IA decida nombre de archivo y contenido
    system_prompt = (
        "Eres un gestor de archivos. Basado en la petición, responde estrictamente en este formato:\n"
        "NOMBRE: [nombre_del_archivo.ext]\n"
        "CONTENIDO: [lo que debe ir dentro]"
    )
    
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': instruccion},
    ])

    respuesta = response['message']['content']
    
    try:
        # Extraer nombre y contenido
        lineas = respuesta.split('\n')
        nombre = lineas[0].replace("NOMBRE:", "").strip()
        contenido = "\n".join(lineas[1:]).replace("CONTENIDO:", "").strip()
        
        ruta_final = os.path.join(CARPETA_PROYECTOS, nombre)
        
        with open(ruta_final, "w", encoding="utf-8") as f:
            f.write(contenido)
            
        print(f"✅ Archivo creado con éxito en: {ruta_final}")
    except Exception as e:
        print(f"❌ Error al interpretar la respuesta de la IA: {e}")

# Ejemplo de uso
print("--- SISTEMA DE GESTIÓN DE ARCHIVOS CON LLAMA 3 ---")
orden = input("¿Qué archivo quieres que cree?: ")
ia_crear_archivos(orden)