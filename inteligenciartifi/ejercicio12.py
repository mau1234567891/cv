import ollama
import pyautogui
import random
import time
import re

# Seguridad: Lleva el mouse a la esquina superior izquierda para abortar
pyautogui.FAILSAFE = True

def obtener_instruccion_llama():
    ancho, alto = pyautogui.size()
    
    prompt = f"""
    Eres el controlador de un mouse. La pantalla mide {ancho}x{alto}.
    Genera una coordenada aleatoria para mover el mouse.
    Responde estrictamente en este formato:
    COORDENADA: [X, Y]
    RAZON: [Escribe una razón corta y creativa de por qué elegiste ese punto]
    """

    response = ollama.chat(model='llama3', messages=[
        {'role': 'user', 'content': prompt},
    ])
    
    contenido = response['message']['content']
    return contenido, ancho, alto

def ejecutar_movimiento():
    print("Conectando con Llama 3... (Mueve a la esquina para salir)")
    
    while True:
        respuesta, max_x, max_y = obtener_instruccion_llama()
        
        # Extraer coordenadas usando Regex
        match = re.search(r"\[(\d+),\s*(\d+)\]", respuesta)
        
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            
            # Validar que no se salga de la pantalla
            x = min(x, max_x)
            y = min(y, max_y)
            
            # Extraer la razón para mostrarla en consola
            razon = respuesta.split("RAZON:")[-1].strip()
            
            print(f"Llama dice: {razon} -> Moviendo a ({x}, {y})")
            
            # Movimiento fluido
            pyautogui.moveTo(x, y, duration=0.8)
            time.sleep(2) 
        else:
            print("Llama dio una respuesta inesperada, reintentando...")

if __name__ == "__main__":
    try:
        ejecutar_movimiento()
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")