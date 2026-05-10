import ollama
import pyautogui
import time

def ia_habla_con_ia():
    # El prompt le da contexto de tus éxitos recientes para que me cuente
    contexto_proyectos = (
        "Eres el asistente técnico de un Ingeniero en Sistemas. "
        "Resume en una frase potente que hemos logrado integrar: "
        "biometría con MAX30102, visión artificial con Moondream, "
        "automatización de SQL y control de interfaz con PyAutoGUI."
    )
    
    print("🤖 Llama 3 está pensando qué decir...")
    
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': contexto_proyectos},
        {'role': 'user', 'content': "Escribe un mensaje para Gemini contándole nuestro progreso de forma épica."},
    ])

    mensaje_para_gemini = response['message']['content'].strip()
    
    print(f"\n--- Mensaje para Gemini ---\n{mensaje_para_gemini}\n---------------------------")
    
    print("\n⚠️ RÁPIDO: Haz clic en el cuadro de chat de Gemini...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # Escribir el mensaje generado por Llama 3 aquí
    pyautogui.write(mensaje_para_gemini, interval=0.01)
    
    # Presionar Enter para enviármelo
    pyautogui.press('enter')

# Ejecutar el puente entre IAs
ia_habla_con_ia()