import ollama
import pyautogui
import time

def buscar_en_google_con_ia(tema_peticion):
    # Configuramos el sistema para que genere términos de búsqueda efectivos
    system_prompt = (
        "Eres un experto en investigación. Transforma la petición del usuario "
        "en una sola frase de búsqueda optimizada para Google. "
        "No respondas con frases largas, SOLO el texto que se debe escribir en el buscador."
    )
    
    print(f"Optimizando búsqueda para: {tema_peticion}...")
    
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': f"Genera una búsqueda para: {tema_peticion}"},
    ])

    termino_busqueda = response['message']['content'].strip().replace('"', '')
    
    print(f"--- Término de Búsqueda ---\n{termino_busqueda}\n-----------------------")
    
    print("Cámbiate al navegador... Tienes 4 segundos.")
    time.sleep(4)
    
    # 1. Atajo para ir a la barra de búsqueda (Ctrl + L o Ctrl + E)
    pyautogui.hotkey('ctrl', 'l') 
    time.sleep(0.5)
    
    # 2. Escribir la búsqueda
    pyautogui.write(termino_busqueda, interval=0.01)
    
    # 3. Presionar Enter
    pyautogui.press('enter')

# Ejemplo de uso
peticion = input("¿Qué quieres que busque la IA?: ")
buscar_en_google_con_ia(peticion)