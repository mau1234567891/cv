import ollama
import time

# Pedir tema de la tarea
tema = input("¿Qué tarea quieres hacer? ")

# Prompt para la IA
prompt = f"Redacta una tarea escolar clara y ordenada sobre: {tema}"

# Consultar a Llama3
respuesta = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'user', 'content': prompt}
    ]
)

texto = respuesta['message']['content']

# Escribir en archivo poco a poco
with open("tarea.txt", "w", encoding="utf-8") as archivo:
    for palabra in texto.split():
        archivo.write(palabra + " ")
        archivo.flush()
        print(palabra, end=" ", flush=True)
        time.sleep(1)

print("\n\nTarea completada y guardada en tarea.txt")