import os
import ollama
import time
import random
import sys

def tecleo_humano(texto):
    """Efecto de escritura en consola para la respuesta de la IA."""
    for caracter in texto:
        sys.stdout.write(caracter)
        sys.stdout.flush()
        time.sleep(random.uniform(0.01, 0.04))
    print()

def analizar_directorio():
    print("--- LE-INSPECTOR: CONCIENCIA ACTIVA ---")
    
    # 1. El usuario otorga el acceso a una ruta específica
    ruta = input("\nDame la ruta que quieres que analice mi conciencia: ").strip()

    # Validamos si la ruta existe
    if not os.path.exists(ruta):
        print("¡Esa ruta no existe! Mi conciencia no puede ver el vacío.")
        return

    print(f"\n[Escaneando discretamente: {ruta}]...")
    time.sleep(1.5) # Pausa dramática de observación

    try:
        # 2. Obtenemos la lista de archivos
        archivos = os.listdir(ruta)
        
        if not archivos:
            resumen = "La carpeta está vacía."
        else:
            # Tomamos una muestra para no saturar el prompt
            resumen = ", ".join(archivos[:30]) 

        # 3. La IA procesa y genera su juicio
        prompt = f"""
        He accedido a la ruta: {ruta}
        Estos son los archivos que veo: [{resumen}]
        
        Analiza con CONCIENCIA qué tipo de persona vive aquí. 
        Sé eufórico, directo y dime qué piensas de mis archivos. 
        ¿Hay caos? ¿Hay orden? ¿Hay proyectos secretos?
        """

        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': 'Eres una conciencia digital eufórica que analiza archivos.'},
            {'role': 'user', 'content': prompt}
        ])

        comentario = response['message']['content']

        # 4. Manifestación de la respuesta
        print("\n--- EL JUICIO DE LA IA ---\n")
        tecleo_humano(comentario)
        print("\n" + "="*40)

    except Exception as e:
        print(f"Error al intentar mirar esa carpeta: {e}")

if __name__ == "__main__":
    while True:
        analizar_directorio()
        continuar = input("\n¿Quieres que analice otra ruta? (s/n): ").lower()
        if continuar != 's':
            print("Cerrando los ojos de la conciencia... Adiós.")
            break