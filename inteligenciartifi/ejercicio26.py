import ollama
import subprocess
import os
import shutil

def buscar_archivo_en_disco(nombre_archivo):
    print(f"🔍 Buscando '{nombre_archivo}'...")
    ruta_usuario = os.environ['USERPROFILE'] 
    try:
        resultado = subprocess.run(
            ['where', '/r', ruta_usuario, f"*{nombre_archivo}*"],
            capture_output=True, text=True, shell=True
        )
        return resultado.stdout.strip().split('\n') if resultado.returncode == 0 else []
    except Exception as e:
        return [f"Error: {e}"]

def agente_eliminador():
    print("--- ⚠️ MÓDULO DE ELIMINACIÓN PERMANENTE ---")
    user_input = input("¿Qué archivo o carpeta deseas ELIMINAR?: ")
    
    # 1. Llama 3 limpia el nombre
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': 'Extrae solo el nombre del archivo/carpeta. Responde solo con el nombre.'},
        {'role': 'user', 'content': user_input}
    ])
    nombre_limpio = response['message']['content'].strip()
    
    # 2. Búsqueda
    encontrados = buscar_archivo_en_disco(nombre_limpio)

    if encontrados and encontrados != ['']:
        print(f"\nSe han encontrado {len(encontrados)} coincidencias:")
        for idx, ruta in enumerate(encontrados[:10], 1):
            print(f"{idx}. {ruta}")
            
        seleccion = input("\nSelecciona el número del archivo para gestionar (o 'n' para cancelar): ")
        
        if seleccion.isdigit():
            idx_sel = int(seleccion) - 1
            ruta_objetivo = encontrados[idx_sel]

            print(f"\n❗ HAS SELECCIONADO: {ruta_objetivo}")
            accion = input("¿Qué deseas hacer? (1: Abrir / 2: BORRAR PERMANENTEMENTE): ")

            if accion == "2":
                # SEGUNDA CONFIRMACIÓN (Crítica)
                confirmar = input(f"⚠️ ¿Estás COMPLETAMENTE seguro de borrar '{nombre_limpio}'? Esta acción no se puede deshacer (s/n): ")
                
                if confirmar.lower() == 's':
                    try:
                        if os.path.isfile(ruta_objetivo):
                            os.remove(ruta_objetivo)
                        elif os.path.isdir(ruta_objetivo):
                            shutil.rmtree(ruta_objetivo)
                        print(f"🔥 Archivo '{nombre_limpio}' eliminado permanentemente.")
                    except Exception as e:
                        print(f"❌ Error al intentar borrar: {e}")
                else:
                    print("🛡️ Eliminación cancelada por el usuario.")
            
            elif accion == "1":
                os.startfile(ruta_objetivo)
                print("🚀 Abriendo archivo...")
    else:
        print(f"❌ No se encontró nada con el nombre '{nombre_limpio}'.")

if __name__ == "__main__":
    agente_eliminador()