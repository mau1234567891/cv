import ollama
import pyautogui
import time
import random
import re

# Seguridad: Si el mouse toca una esquina, el script se detiene
pyautogui.FAILSAFE = True

# Coordenadas del lienzo (1214x671)
LIENZO_ANCHO = 1214
LIENZO_ALTO = 671
CENTRO_X = LIENZO_ANCHO // 2
CENTRO_Y = LIENZO_ALTO // 2

def obtener_instruccion_loca():
    # Prompt para que Llama 3 genere coordenadas de "ataque" al lienzo
    prompt = f"""
    ¡EUFORIA TOTAL! Genera un punto de ataque en el lienzo de {LIENZO_ANCHO}x{LIENZO_ALTO}.
    Responde estrictamente:
    PUNTO: [X, Y]
    GRITO: [Frase corta de locura]
    """
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': 'Eres un pincel con vida propia y mucha energía.'},
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    except Exception:
        return None

def hacer_garabato(x_destino, y_destino):
    # Mover al punto sin dibujar
    pyautogui.moveTo(x_destino, y_destino, duration=0.1)
    
    # Empezar a rayar
    pyautogui.mouseDown(button='left')
    
    # Hacemos 3 o 4 movimientos rápidos y aleatorios cerca del punto
    for _ in range(4):
        offset_x = random.randint(-40, 40)
        offset_y = random.randint(-40, 40)
        pyautogui.moveRel(offset_x, offset_y, duration=0.1)
    
    # Soltamos el pincel
    pyautogui.mouseUp(button='left')

def ejecutar_bucle_artistico():
    print("--- INICIANDO CAOS EN PAINT ---")
    print("Regresando al centro después de cada trazo...")
    time.sleep(3) # Tiempo para que pongas Paint al frente

    while True:
        res = obtener_instruccion_loca()
        
        if res:
            match = re.search(r"PUNTO:\s*\[(\d+),\s*(\d+)\]", res)
            grito = res.split("GRITO:")[-1].strip() if "GRITO:" in res else "¡ZAS!"
            
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                
                # Limitar coordenadas para no salirnos del lienzo
                x = max(100, min(x, 1100))
                y = max(200, min(y, 600))

                print(f"Llama 3: {grito} -> Atacando ({x}, {y})")
                
                # Acción de dibujo
                hacer_garabato(x, y)
                
                # REQUISITO: Regresar al centro automáticamente
                pyautogui.moveTo(CENTRO_X, CENTRO_Y, duration=0.2)

        # Espera de 2 segundos para no saturar tu Ryzen/laptop
        time.sleep(2)

if __name__ == "__main__":
    try:
        ejecutar_bucle_artistico()
    except (KeyboardInterrupt, pyautogui.FailSafeException):
        print("\nCaos detenido.")