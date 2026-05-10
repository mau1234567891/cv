import ollama
import subprocess
import os
import shutil

def buscar_en_disco(nombre_archivo):
    ruta_usuario = os.environ['USERPROFILE']
    print(f"🔍 Buscando '{nombre_archivo}'...")
    try:
        resultado = subprocess.run(
            ['where', '/r', ruta_usuario, f"*{nombre_archivo}*"],
            capture_output=True, text=True, shell=True
        )
        return resultado.stdout.strip().split('\n') if resultado.returncode == 0 else []
    except:
        return []

def gestionar_archivo():
    user_input = input("\n📝 ¿Qué archivo buscas?: ")
    
    # Llama 3 extrae el nombre clave
    res = ollama.chat(model='llama3', messages=[
        {'role': 'user', 'content': f"Extrae solo el nombre de archivo de: '{user_input}'. Solo el nombre."}
    ])
    nombre_limpio = res['message']['content'].strip()
    
    archivos = buscar_en_disco(nombre_limpio)

    if not archivos or archivos == ['']:
        print("❌ No encontré nada.")
        return

    print(f"\n📂 Resultados encontrados:")
    for i, ruta in enumerate(archivos[:5], 1):
        print(f"{i}. {ruta}")

    print("\n--- ACCIONES ---")
    print("1. Abrir archivo")
    print("2. Ver ubicación")
    print("3. COPIAR Y PEGAR en otra carpeta") # La opción que pediste
    
    try:
        opcion = input("\nElige una opción (1-3): ")
        
        if opcion == "3":
            # Lógica de Copiar y Pegar
            archivo_origen = archivos[0] # Tomamos el primero de la lista por defecto
            destino = input("📍 Pega la ruta de la carpeta destino: ").strip()
            
            if not os.path.exists(destino):
                os.makedirs(destino)
                print(f"📁 Carpeta creada: {destino}")

            nombre_base = os.path.basename(archivo_origen)
            ruta_final = os.path.join(destino, nombre_base)
            
            shutil.copy2(archivo_origen, ruta_final) # copy2 mantiene metadatos
            print(f"✅ ¡Copiado con éxito a: {ruta_final}!")

        elif opcion == "1":
            os.startfile(archivos[0])
        elif opcion == "2":
            subprocess.run(f'explorer /select,"{archivos[0]}"')
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    gestionar_archivo()