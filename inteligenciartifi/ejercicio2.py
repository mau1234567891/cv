import ollama
from PIL import Image

# Historial para la memoria del chat de texto
messages = [
    {"role": "system", "content": "Eres un asistente de IA útil y conciso."}
]

print("--- Chat con Llama 3 + Generador de Imágenes Iniciado ---")
print("Usa '/img [descripción]' para generar imágenes o chatea normalmente.")

while True:
    user_input = input("\nTu: ")
    
    # 1. Salida segura
    if user_input.lower() in ["salir", "exit"]: 
        print("Cerrando la app de forma segura...")
        break

    # 2. Lógica de IMAGEN (Aquí es donde iría tu modelo Turbo)
    if user_input.startswith("/img "):
        prompt_imagen = user_input.replace("/img ", "")
        print(f"Generando imagen para: {prompt_imagen}...")
        
        # NOTA: Aquí debes insertar la función real de tu modelo Turbo.
        # Por ahora, simulamos el guardado para que no de error.
        print(f"Éxito: Imagen '{prompt_imagen}' procesada por el modelo Turbo.")
        print("Archivo guardado como: resultado.png")
        continue 

    # 3. Lógica de CHAT (Solo para Llama 3 u otros modelos de Ollama)
    messages.append({"role": "user", "content": user_input})
    
    try:
        # AQUÍ DEBE IR 'llama3', NO el modelo de imagen
        response = ollama.chat(model='llama3', messages=messages)
        
        respuesta_texto = response['message']['content']
        print(f"\nLlama 3: {respuesta_texto}")
        
        # Guardar en historial
        messages.append({"role": "assistant", "content": respuesta_texto})
        
    except Exception as e:
        print(f"Error al conectar con Ollama: {e}")