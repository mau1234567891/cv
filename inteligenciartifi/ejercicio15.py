import ollama
import pyautogui
import time
import random

# Configuración de seguridad
pyautogui.FAILSAFE = True

def escritura_humana(texto):
    """Escribe el texto simulando pulsaciones humanas."""
    for letra in texto:
        # Escribe la letra
        pyautogui.write(letra)
        
        # Simula el tiempo que tarda un dedo en pasar a la siguiente tecla
        # Entre 0.05 y 0.2 segundos es una velocidad de escritura humana normal/rápida
        tiempo_espera = random.uniform(0.05, 0.15)
        
        # A veces las personas dudan, añadimos una pausa más larga ocasional
        if random.random() < 0.05: # 5% de probabilidad de "dudar"
            tiempo_espera += random.uniform(0.3, 0.6)
            
        time.sleep(tiempo_espera)

def obtener_texto_de_llama():
    prompt = "Escribe un párrafo corto y creativo sobre por qué la tecnología es fascinante. Sé eufórico."
    
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': 'Eres un redactor muy veloz y entusiasta.'},
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    except Exception as e:
        print(f"Error con Ollama: {e}")
        return None

def ejecutar_asistente_word():
    print("--- ASISTENTE DE ESCRITURA MANUAL ---")
    print("Abre Word y pon el cursor donde quieras escribir.")
    
    # Te damos 5 segundos para que hagas clic en Word
    for i in range(5, 0, -1):
        print(f"Empezando en {i}...")
        time.sleep(1)

    while True:
        # 1. Llama 3 piensa qué decir
        texto_para_escribir = obtener_texto_de_llama()
        
        if texto_para_escribir:
            print("Escribiendo contenido generado por Llama 3...")
            # 2. Escribimos letra por letra
            escritura_humana(texto_para_escribir)
            
            # 3. Presionamos Enter un par de veces para el siguiente párrafo
            pyautogui.press('enter')
            pyautogui.press('enter')
        
        # Esperamos los 2 segundos que pediste para no saturar la PC
        print("Esperando 2 segundos para el siguiente pensamiento...")
        time.sleep(2)

if __name__ == "__main__":
    try:
        ejecutar_asistente_word()
    except pyautogui.FailSafeException:
        print("\nEscritura abortada (moviste el mouse a la esquina).")
    except KeyboardInterrupt:
        print("\nAsistente apagado.")