import ollama

def asistente_matematicas_streaming():
    print("--- Tutor de Matemáticas (Modo Fluido) ---")
    print("Escribe 'salir' para finalizar.\n")
    
    system_prompt = (
    "Eres un profesor de matemáticas de secundaria. "
    "Tu estilo es motivador y usas analogías (como la de la balanza). "
    "Usa siempre este formato: "
    "1. Concepto rápido. "
    "2. Resolución paso a paso usando fórmulas matemáticas. "
    "3. Un pequeño reto al final para el alumno."
    )

    historial = [{'role': 'system', 'content': system_prompt}]

    while True:
        pregunta = input("Alumno: ")
        if pregunta.lower() in ['salir', 'exit']: break

        historial.append({'role': 'user', 'content': pregunta})
        
        print("\nProfesor: ", end='', flush=True)
        
        respuesta_completa = ""
        
        try:
            # Activamos el streaming para no saturar la memoria
            for chunk in ollama.chat(model='llama3', messages=historial, stream=True):
                contenido = chunk['message']['content']
                print(contenido, end='', flush=True)
                respuesta_completa += contenido
            
            print("\n") # Salto de línea al terminar
            historial.append({'role': 'assistant', 'content': respuesta_completa})

        except Exception as e:
            print(f"\nError: {e}")
            break

if __name__ == "__main__":
    asistente_matematicas_streaming()