import ollama
import pyautogui
import time
import os

# Configuración
ARCHIVO_VIGILADO = "ejercicio46.py"
ULTIMA_MODIFICACION = 0

def procesar_instruccion(texto):
    print(f"🤖 Llama 3 analizando: {texto}")
    
    system_prompt = (
        "Eres un operador de sistemas autónomo. "
        "Si el usuario pide una búsqueda, responde: 'BUSCAR: [término]'. "
        "Si el usuario pide un mensaje, responde: 'MENSAJE: [texto]'. "
        "Si es una duda técnica, responde: 'EXPLICAR: [respuesta]'."
    )
    
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': texto},
    ])
    
    decision = response['message']['content'].strip()
    ejecutar_accion(decision)

def ejecutar_accion(decision):
    print(f"⚡ Ejecutando: {decision}")
    
    # Lógica de decisión
    if "BUSCAR:" in decision:
        busqueda = decision.split("BUSCAR:")[1].strip()
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        pyautogui.write(busqueda, interval=0.01)
        pyautogui.press('enter')
        
    elif "MENSAJE:" in decision:
        msg = decision.split("MENSAJE:")[1].strip()
        pyautogui.write(msg, interval=0.01)
        pyautogui.press('enter')

print(f"👀 Vigilando {ARCHIVO_VIGILADO}... Escribe algo y guarda el archivo.")

# Bucle infinito de vigilancia
while True:
    if os.path.exists(ARCHIVO_VIGILADO):
        mtime = os.path.getmtime(ARCHIVO_VIGILADO)
        if mtime > ULTIMA_MODIFICACION:
            ULTIMA_MODIFICACION = mtime
            
            with open(ARCHIVO_VIGILADO, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                
            if contenido:
                procesar_instruccion(contenido)
    
    time.sleep(1) # Pausa para no saturar el procesador