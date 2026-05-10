import ollama
import pyautogui
import time

def generar_y_escribir_sql(prompt_usuario):
    # Configuramos el sistema para que Llama 3 solo entregue código SQL puro
    system_prompt = "Eres un experto en PostgreSQL. Devuelve ÚNICAMENTE el código SQL solicitado, sin explicaciones ni bloques de texto."
    
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': f"Crea el siguiente código SQL: {prompt_usuario}"},
    ])

    codigo_sql = response['message']['content'].strip()
    
    # Limpieza básica para quitar bloques de markdown si el modelo los incluye
    codigo_sql = codigo_sql.replace('```sql', '').replace('```', '')

    print(f"--- Código Generado ---\n{codigo_sql}\n-----------------------")
    
    # Tiempo para que cambies a la ventana de pgAdmin
    print("Cámbiate a pgAdmin... Tienes 3 segundos.")
    time.sleep(3)
    
    # Escribir el código en la posición actual del cursor
    pyautogui.write(codigo_sql, interval=0.01)

# Ejemplo de uso
peticion = input("¿Qué SQL necesitas generar?: ")
generar_y_escribir_sql(peticion)