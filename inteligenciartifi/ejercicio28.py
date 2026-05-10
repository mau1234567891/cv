import ollama
import os

def reparar_cualquier_archivo():
    print("--- 🛠️  BIENVENIDO AL REPARADOR DE CÓDIGO (Ryzen 7 Edition) ---")
    
    # 1. Pedir al usuario el nombre del archivo
    archivo_objetivo = input("\n📄 Escribe el nombre o la ruta del archivo .py que quieres reparar: ").strip()

    # Si el usuario no puso la extensión .py, se la agregamos
    if not archivo_objetivo.endswith('.py'):
        archivo_objetivo += '.py'

    if not os.path.exists(archivo_objetivo):
        print(f"❌ Error: El archivo '{archivo_objetivo}' no existe en esta carpeta.")
        return

    # 2. Leer el contenido
    with open(archivo_objetivo, 'r', encoding='utf-8') as f:
        codigo_sucio = f.read()

    print(f"🧠 Llama 3 analizando '{archivo_objetivo}'...")

    # 3. Pedir la reparación a Llama 3
    prompt = (
        "Actúa como un desarrollador Senior. Refactoriza el siguiente código: "
        "1. Mejora los nombres de variables. "
        "2. Optimiza la lógica. "
        "3. Asegúrate de que los cálculos numéricos sean precisos y limpios. "
        "4. Devuelve ÚNICAMENTE el código resultante, sin explicaciones.\n\n"
        f"CÓDIGO:\n{codigo_sucio}"
    )

    try:
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        codigo_reparado = response['message']['content']

        # 4. Guardar el resultado en un archivo nuevo
        nombre_salida = archivo_objetivo.replace(".py", "_reparado.py")
        with open(nombre_salida, 'w', encoding='utf-8') as f:
            f.write(codigo_reparado)
        
        print(f"\n✅ ¡Éxito! El código ha mejorado considerablemente.")
        print(f"📂 Archivo generado: {nombre_salida}")
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Ocurrió un error con Ollama: {e}")

if __name__ == "__main__":
    reparar_cualquier_archivo()