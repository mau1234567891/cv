import ollama
import pyautogui
import pygetwindow as gw # Necesitas instalar: pip install pygetwindow
import pyperclip         # Necesitas instalar: pip install pyperclip
import time

# Configuración de memoria del bot
ULTIMA_VENTANA = ""
ULTIMO_PORTAPAPELES = ""

def pensar_segun_contexto(ventana, contenido):
    print(f"🧠 Llama 3 analizando contexto: {ventana}")
    
    system_prompt = (
        "Eres un asistente invisible que vigila la PC. "
        "Si el usuario está en un navegador, ofrece búsquedas. "
        "Si está en un editor, ofrece código. "
        "Si copió un texto, ofrece resumirlo o enviarlo."
        "Responde con: 'ACCION: [tu sugerencia]'"
    )
    
    prompt_usuario = f"Estoy en la ventana: '{ventana}'. He copiado esto: '{contenido}'. ¿Qué debo hacer?"
    
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt_usuario},
    ])

    decision = response['message']['content'].strip()
    print(f"🤖 Sugerencia: {decision}")

print("🚀 Sistema de Vigilancia Total iniciado...")

while True:
    try:
        # 1. Obtener la ventana activa
        ventana_activa = gw.getActiveWindowTitle()
        
        # 2. Obtener contenido del portapapeles
        contenido_clipboard = pyperclip.paste()

        # Solo actúa si la ventana cambió o si hay algo nuevo en el portapapeles
        if ventana_activa != ULTIMA_VENTANA or contenido_clipboard != ULTIMO_PORTAPAPELES:
            
            if ventana_activa and (ventana_activa != ULTIMA_VENTANA):
                print(f"👀 Detectado cambio a: {ventana_activa}")
                ULTIMA_VENTANA = ventana_activa
            
            if contenido_clipboard != ULTIMO_PORTAPAPELES:
                print(f"📋 Nuevo contenido copiado: {contenido_clipboard[:30]}...")
                ULTIMO_PORTAPAPELES = contenido_clipboard
                
                # Llamamos a Llama 3 cuando detectamos que copiaste algo importante
                pensar_segun_contexto(ventana_activa, contenido_clipboard)

    except Exception as e:
        # A veces al cambiar de ventana muy rápido da error de acceso
        pass

    time.sleep(4) # Respiro para el CPU