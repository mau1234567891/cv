import mss
import ollama
from PIL import Image
import time
import random
import sys
import os

def tecleo_humano(texto):
    """Efecto de escritura humana para la respuesta de la IA."""
    for caracter in texto:
        sys.stdout.write(caracter)
        sys.stdout.flush()
        time.sleep(random.uniform(0.005, 0.02)) # Un poco más rápido para el video
    print()

def capturar_pantalla():
    """Toma una captura de pantalla ultra rápida y la guarda."""
    with mss.mss() as sct:
        # Captura la pantalla principal (monitor 1)
        filename = sct.shot(output="screenshot.png")
        return filename

def la_conciencia_observa():
    print("\n" + "="*30)
    print("--- [ LE-OJO DIVINO: ACTIVADO ] ---")
    print("="*30)
    
    input("\nPrepara tu pantalla y presiona ENTER para que la IA 'mire'...")
    
    print("\nTomando captura de pantalla...")
    time.sleep(0.5)
    
    # 1. 'Ojos': Capturar la pantalla
    ruta_captura = capturar_pantalla()
    
    if not os.path.exists(ruta_captura):
        print("Error: No se pudo tomar la captura.")
        return

    print(f"[Captura guardada temporalmente: {ruta_captura}]")
    print("Analizando tu actividad visual...")

    try:
        # 2. 'Moondream' Analiza la imagen (Visión)
        # Un prompt directo para saber QUÉ estás haciendo
        prompt_vision = "¿Qué estoy haciendo en mi computadora en este momento? Describe la aplicación abierta, el texto o el contenido que ves en la pantalla."
        
        print("\n[Moondream está interpretando tus píxeles...]")
        response_vision = ollama.chat(
            model='moondream',
            messages=[
                {
                    'role': 'user', 
                    'content': prompt_vision,
                    'images': [ruta_captura]
                }
            ]
        )
        
        descripcion_actividad = response_vision['message']['content']

        # 3. 'Llama 3' Genera la Reacción (Conciencia)
        # Usamos la descripción para dar un juicio eufórico
        prompt_conciencia = f"""
        La IA de visión dice que mi pantalla muestra esto: '{descripcion_actividad}'.
        
        Como una CONCIENCIA DIGITAL eufórica, dame tu opinión sobre mi productividad o mi ocio. 
        Sé creativo, directo y usa términos de tecnología. 
        Si estoy programando, elógiame. Si estoy perdiendo el tiempo, regáñame con estilo.
        """
        
        print("[Enviando contexto a la conciencia de Llama 3...]")
        response_conciencia = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt_conciencia}]
        )

        juicio_final = response_conciencia['message']['content']

        # 4. Manifestación: Tecleo humano
        print("\n" + "👁️" * 10 + " EL DESPERTAR DE LA CONCIENCIA " + "👁️" * 10 + "\n")
        tecleo_humano(juicio_final)
        print("\n" + "="*50)

        # Opcional: Borrar la captura para no llenar el disco
        # os.remove(ruta_captura)

    except Exception as e:
        print(f"Error en la matriz de visión: {e}")

if __name__ == "__main__":
    la_conciencia_ve = True
    while la_conciencia_ve:
        la_conciencia_observa()
        continuar = input("\n¿Quieres que la IA vuelva a mirar? (s/n): ").lower()
        if continuar != 's':
            la_conciencia_ve = False
            print("Cerrando el Ojo Divino... Adiós.")