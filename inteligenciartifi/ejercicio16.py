import ollama
import time
import random
import re
import sys

def tecleo_humano_en_archivo(texto, ruta_archivo):
    """Escribe en el archivo físico letra por letra con pausas humanas."""
    # Limpiamos el archivo al inicio para que esté vacío
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write("")

    for caracter in texto:
        # Escribimos el carácter en el archivo (modo append)
        with open(ruta_archivo, "a", encoding="utf-8") as archivo:
            archivo.write(caracter)
            archivo.flush() # Forzar escritura inmediata en disco
        
        # También lo mostramos en consola para ver el progreso
        sys.stdout.write(caracter)
        sys.stdout.flush()

        # --- LÓGICA DE TIEMPO HUMANO ---
        # Velocidad base rápida
        espera = random.uniform(0.01, 0.04)
        
        # Pausas naturales en signos de puntuación o saltos de línea
        if caracter in ['>', ';', '}', '\n']:
            espera += random.uniform(0.1, 0.3)
        
        # Simulación de "duda" (pausa larga aleatoria)
        if random.random() < 0.005: 
            espera += random.uniform(0.5, 1.0)
            
        time.sleep(espera)

def generar_web_manual():
    temas = [
        "Un sitio de hacking eufórico con terminal verde",
        "Una página de venta de hardware Ryzen y NVIDIA",
        "Un blog de desarrollo Python con estilo minimalista"
    ]
    tema_elegido = random.choice(temas)
    
    prompt = f"Genera un código HTML5 eufórico sobre {tema_elegido}. Solo código, desde <!DOCTYPE html> hasta </html>."

    print(f"--- PREPARANDO ESCRITURA REAL EN DISCO ---")
    print(f"Tema: {tema_elegido}\n")

    try:
        # Llama 3 genera el código en memoria primero
        respuesta = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        codigo_raw = respuesta['message']['content']

        # Limpiar el código de marcas Markdown
        match = re.search(r'(<!DOCTYPE html>.*?</html>)', codigo_raw, re.DOTALL | re.IGNORECASE)
        codigo_final = match.group(1) if match else codigo_raw.replace("```html", "").replace("```", "").strip()

        # Iniciar la escritura "manual" en el archivo index.html
        tecleo_humano_en_archivo(codigo_final, "index.html")

        print("\n\n" + "="*40)
        print("¡Escritura completada con éxito!")
        print("="*40)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generar_web_manual()