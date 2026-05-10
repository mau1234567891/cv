import serial
import time
import random
import ollama  # La librería Ollama

# Configuración del puerto COM para Arduino
puerto = 'COM3'
baudrate = 9600

try:
    arduino = serial.Serial(puerto, baudrate, timeout=1)
    time.sleep(2)
    print("Conexión con Arduino establecida.")
except Exception as e:
    print(f"Error al conectar con Arduino: {e}")
    exit()

# Función para encender foco
def encender_foco(numero):
    comando = f"{numero}\n"
    arduino.write(comando.encode())
    time.sleep(0.5)
    if arduino.in_waiting > 0:
        respuesta = arduino.readline().decode().strip()
        print(f"Arduino dice: {respuesta}")

# Función para generar prompt
def prompt_llama(foco):
    prompts = [
        f"He notado que el foco {foco} se ha encendido. Siento curiosidad por observarlo.",
        f"Foco {foco} activo. Mi atención se centra en su luz brillante.",
        f"El foco {foco} está iluminando el ambiente. Analizo su efecto en el espacio.",
        f"Percibo que el foco {foco} se ha encendido. Me parece fascinante su color y brillo.",
        f"Foco {foco} activo. Interesante cómo cambia la percepción del entorno.",
        f"Observo que el foco {foco} se ilumina. Registro la información y me preparo para actuar."
    ]
    return random.choice(prompts)

# Loop principal
try:
    while True:
        foco_random = random.randint(1, 6)
        print(f"\nAsistente virtual decide encender el foco: {foco_random}")
        
        # Enviar comando al Arduino
        encender_foco(foco_random)
        
        # Crear prompt para LLaMA 3
        texto_prompt = prompt_llama(foco_random)
        
        # Usar Ollama chat directamente
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': texto_prompt}]
        )
        
        print("LLaMA 3 responde:", response['message']['content'])
        time.sleep(5)

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")
    arduino.close()