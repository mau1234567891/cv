import ollama
import time

# 1. Pedir el tema del sitio web
tema = input("¿Sobre qué quieres crear la página web? ")

# 2. Refinamos el prompt para que la IA responda SOLO con código HTML/CSS
prompt = f"Crea el código de una página web completa (HTML y CSS incluido en <style>) sobre: {tema}. Devuelve solo el código, sin explicaciones."

print(f"\nGenerando código para: {tema}...\n")

# 3. Consultar a Llama3
respuesta = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'user', 'content': prompt}
    ]
)

texto = respuesta['message']['content']

# 4. Guardar como archivo .html y mostrar efecto de escritura
# Cambiamos "tarea.txt" por "index.html"
with open("index.html", "w", encoding="utf-8") as archivo:
    # Dividimos por líneas para que el código no se rompa y sea legible al imprimir
    for linea in texto.splitlines():
        archivo.write(linea + "\n")
        archivo.flush()
        print(linea)
        # Un delay más corto (0.1) porque el código suele ser largo
        time.sleep(0.1) 

print("\n" + "="*30)
print("¡Página web generada con éxito!")
print("Archivo guardado como: index.html")
print("="*30)