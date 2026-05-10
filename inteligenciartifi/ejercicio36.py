import ollama
import os
import subprocess

def buscar_y_abrir_carpeta(nombre):
    # Definimos dónde buscar (puedes poner 'C:/' pero tardará mucho, mejor carpetas clave)
    rutas_clave = [os.path.expanduser("~/Desktop"), os.path.expanduser("~/Documents")]
    print(f"[Sistema] Buscando: {nombre}...")
    
    for ruta in rutas_clave:
        for raiz, _, archivos in os.walk(ruta):
            for archivo in archivos:
                if nombre.lower() in archivo.lower():
                    ruta_completa = os.path.normpath(os.path.join(raiz, archivo))
                    subprocess.run(['explorer', '/select,', ruta_completa])
                    return f"✅ Archivo encontrado y carpeta abierta: {archivo}"
    return "❌ No pude encontrar ese archivo en tus carpetas principales."

def ejecutar_app(app_nombre):
    print(f"[Sistema] Intentando abrir: {app_nombre}...")
    # Intenta ejecutar directamente por nombre (funciona con apps en el PATH como chrome, notepad, calc)
    try:
        subprocess.Popen(app_nombre, shell=True)
        return f"🚀 Abriendo {app_nombre}..."
    except Exception as e:
        return f"⚠️ Error al intentar abrir la app: {e}"

# --- Bucle de Mensajes ---
print("--- Asistente Local Activado (Escribe 'salir' para cerrar) ---")

while True:
    orden_usuario = input("\n¿Qué necesitas?: ")
    
    if orden_usuario.lower() in ['salir', 'exit', 'quit']:
        break

    # Llama 3 decide qué hacer
    prompt_sistema = (
        "Eres un controlador de sistema. Tu respuesta debe ser corta y seguir este formato:\n"
        "Si el usuario quiere encontrar un archivo: ACCION: BUSCAR | OBJETO: nombre_del_archivo\n"
        "Si el usuario quiere abrir un programa: ACCION: EJECUTAR | OBJETO: nombre_del_programa\n"
        "Si es una charla normal: ACCION: CHARLAR | OBJETO: respuesta_amistosa"
    )

    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': prompt_sistema},
        {'role': 'user', 'content': orden_usuario},
    ])

    respuesta_ia = response['message']['content']
    
    # Procesamos la decisión de la IA
    if "ACCION: BUSCAR" in respuesta_ia:
        objeto = respuesta_ia.split("|")[1].replace("OBJETO:", "").strip()
        print(buscar_y_abrir_carpeta(objeto))
        
    elif "ACCION: EJECUTAR" in respuesta_ia:
        objeto = respuesta_ia.split("|")[1].replace("OBJETO:", "").strip()
        print(ejecutar_app(objeto))
        
    else:
        print(f"IA: {respuesta_ia}")