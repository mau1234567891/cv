import ollama
import pyautogui
import time

def generar_y_enviar_mensaje(tema_o_busqueda):
    # Configuramos el sistema para que actúe como un asistente de chat fluido
    system_prompt = (
        "Eres un asistente conversacional ingenioso y claro. "
        "Responde de forma natural sobre el tema que se te pide, "
        "mantén la respuesta concisa para que quepa bien en un chat."
    )
    
    print(f"Generando respuesta sobre: {tema_o_busqueda}...")
    
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': f"Escribe un mensaje corto sobre: {tema_o_busqueda}"},
    ])

    mensaje = response['message']['content'].strip()
    
    print(f"--- Mensaje Preparado ---\n{mensaje}\n-----------------------")
    
    # Tiempo para que hagas clic en el cuadro de texto de WhatsApp Web
    print("Haz clic en el chat de WhatsApp... Tienes 5 segundos.")
    time.sleep(5)
    
    # Escribir el mensaje
    # Nota: interval=0.01 ayuda a que no parezca un bot bloqueado por el navegador
    pyautogui.write(mensaje, interval=0.01)
    
    # Opcional: Presionar 'enter' para enviar automáticamente
    pyautogui.press('enter')

# Ejemplo de uso
tema = input("¿De qué quieres que hable el bot?: ")
generar_y_enviar_mensaje(tema)