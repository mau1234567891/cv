import ollama

# Historial para la memoria
messages = [
    {"role": "system", "content": "Eres un asistente de IA útil y conciso."}
]

print("--- Chat con Ollama (Llama 3) Iniciado ---")

while True:
    user_input = input("\nTu: ")
    if user_input.lower() in ["salir", "exit"]: break

    messages.append({"role": "user", "content": user_input})

    # Llamada simplificada a Ollama
    response = ollama.chat(model='llama3', messages=messages)

    respuesta_texto = response['message']['content']
    print(f"\nLlama 3: {respuesta_texto}")

    # Guardar en historial
    messages.append({"role": "assistant", "content": respuesta_texto})