import ollama
import os

def renombrar_local():
    # Carpeta del script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Listar archivos ignorando el propio script
    archivos = [f for f in os.listdir(directorio_actual) 
                if os.path.isfile(os.path.join(directorio_actual, f)) 
                and f != os.path.basename(__file__)]
    
    if not archivos:
        return

    # Mostrar lista para referencia
    for i, archivo in enumerate(archivos):
        print(f"{i+1}. {archivo}")

    seleccion_usuario = input("\nSelecciona el número o escribe el nombre: ").strip()

    archivo_objetivo = None

    # Lógica dual: buscar por número o por nombre
    if seleccion_usuario.isdigit():
        idx = int(seleccion_usuario) - 1
        if 0 <= idx < len(archivos):
            archivo_objetivo = archivos[idx]
    else:
        # Si escribió el nombre, verificamos si existe en la lista
        if seleccion_usuario in archivos:
            archivo_objetivo = seleccion_usuario
        else:
            # Intento de coincidencia parcial por si copió mal
            for f in archivos:
                if seleccion_usuario.lower() in f.lower():
                    archivo_objetivo = f
                    break

    if not archivo_objetivo:
        print("Selección no válida.")
        return

    # Consultar a Llama 3
    prompt = f"Genera un nombre creativo y corto para el archivo '{archivo_objetivo}'. Responde solo el nombre, sin extensión."

    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': 'Eres un gestor de archivos creativo.'},
            {'role': 'user', 'content': prompt},
        ])
        
        sugerencia = response['message']['content'].strip()
        # Limpiar sugerencia de Llama3 (quitar puntos, exclamaciones al inicio, etc.)
        sugerencia_limpia = re.sub(r'[^\w\s-]', '', sugerencia).split('\n')[0]
        
        # REGLA: Le + nombre en minúsculas
        extension = os.path.splitext(archivo_objetivo)[1]
        nuevo_nombre = "Le" + sugerencia_limpia.lower().replace(" ", "-") + extension
        
        os.rename(
            os.path.join(directorio_actual, archivo_objetivo),
            os.path.join(directorio_actual, nuevo_nombre)
        )
        
    except Exception:
        pass

if __name__ == "__main__":
    import re # Necesario para la limpieza de nombre
    renombrar_local()