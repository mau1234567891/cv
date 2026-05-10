import ollama
import pyautogui
import time

def inyectar_codigo_en_colab(peticion):
    # 1. Le pedimos a Llama 3 que genere el código Python para Colab
    system_prompt = (
        "Eres un experto en Python para Google Colab. "
        "Genera solo el código, sin explicaciones. "
        "Si necesitas instalar algo, usa !pip install."
    )
    
    print(f"🤖 Llama 3 procesando lógica para Colab...")
    
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': f"Escribe el código para: {peticion}"},
    ])

    codigo = response['message']['content'].strip()
    # Limpiar bloques de markdown si aparecen
    codigo = codigo.replace('```python', '').replace('```', '')

    print("\n--- Código a Inyectar ---")
    print(codigo)
    print("------------------------\n")

    # 2. Fase de ejecución en la interfaz
    print("⚠️ Tienes 5 segundos para hacer clic en una celda vacía de Colab...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    # 3. Escribir el código en la celda activa
    # Usamos un intervalo pequeño para que la interfaz de Google no se bloquee
    pyautogui.write(codigo, interval=0.005)

    # 4. Atajo de teclado para ejecutar la celda (Ctrl + Enter)
    print("🚀 Ejecutando celda...")
    pyautogui.hotkey('ctrl', 'enter')

# Ejemplo de uso
tarea = input("¿Qué quieres que la IA programe y ejecute en Colab?: ")
inyectar_codigo_en_colab(tarea)