import ollama
import random
import time
from pymongo import MongoClient
from datetime import datetime

# 1. Configuración de MongoDB
uri = "mongodb+srv://mauricioalexander27121999:khHHtiELxLC85Q6@cluster0.l7i0y.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["ia12"]
collection = db["Index"]

def obtener_frase_cmd(comando):
    prompts = [
        f"Inyectando comando en la terminal: {comando}. Ejecución preparada.",
        f"Sintaxis detectada: {comando}. Enviando al kernel del sistema.",
        f"Comando {comando} procesado. Registro de consola actualizado.",
        f"Se ha generado la instrucción: {comando}. Memoria de comandos activa.",
        f"Monitoreando salida de CMD: {comando}. El sistema responde correctamente.",
        f"Nueva línea de comandos lista: {comando}. Procediendo con el registro en la BD."
    ]
    return random.choice(prompts)

# Prompt del sistema refinado para mayor precisión
system_prompt = (
    "Eres un generador automático de scripts CMD para Windows. "
    "Tu tarea es inventar comandos útiles (mkdir, echo, del, type nul, systeminfo, etc.) "
    "y asociarlos a nombres de archivos .txt aleatorios. "
    "RESPUESTA ÚNICA: Solo el comando y el archivo. Ejemplo: mkdir carpeta_test & echo > log.txt"
)

print("--- Generador Automático de Logs (Llama 3 -> MongoDB) ---")
print("Presiona Ctrl+C para detener el proceso.")

try:
    while True:
        # En lugar de input(), le pedimos directamente a Llama que actúe
        # Usamos un mensaje de usuario genérico para "activar" la IA
        try:
            response = ollama.chat(model='llama3', messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Genera el siguiente comando de la secuencia."}
            ])
            
            cmd_generado = response['message']['content'].strip()

            # Evitar logs vacíos
            if cmd_generado:
                frase_tecnica = obtener_frase_cmd(cmd_generado)
                print(f"\n[IA] Generado: {cmd_generado}")
                print(f"> {frase_tecnica}")

                # Guardar en MongoDB
                collection.insert_one({
                    "comando_puro": cmd_generado,
                    "log_consola": frase_tecnica,
                    "timestamp": datetime.now()
                })
                print("[DB] Entry log: OK.")
            
            # Pausa de seguridad para no saturar la CPU o la base de datos
            time.sleep(2) 

        except Exception as e:
            print(f"Error en el ciclo de IA: {e}")
            time.sleep(5)

except KeyboardInterrupt:
    print("\nDeteniendo el generador...")

print("Sistema desconectado.")