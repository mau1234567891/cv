import serial
import ollama
import time

# Configuración del puerto (ajusta el COM a tu laptop)
ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)

def consultar_llama(red, ir):
    prompt = f"""
    Analiza estos datos de un sensor MAX30102:
    Valor Rojo: {red}
    Valor Infrarrojo: {ir}
    
    Dame un argumento breve (máximo 2 oraciones) sobre la estabilidad de la lectura 
    y qué indica una señal IR mayor a la Roja en términos de oxigenación básica.
    """
    
    try:
        response = ollama.generate(model='llama3', prompt=prompt)
        return response['response']
    except Exception as e:
        return "Error conectando con Ollama."

print("Esperando datos del sensor...")

try:
    contador_lecturas = 0
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if "," in line:
                red, ir = line.split(',')
                contador_lecturas += 1
                
                # Para no saturar la RAM y el procesador, consultamos a Llama cada 100 lecturas
                if contador_lecturas >= 100:
                    print(f"\n[DATOS] Rojo: {red} | IR: {ir}")
                    print("[LLAMA 3 DICE]:", consultar_llama(red, ir))
                    print("-" * 30)
                    contador_lecturas = 0
                    
except KeyboardInterrupt:
    print("\nDeteniendo...")
    ser.close()