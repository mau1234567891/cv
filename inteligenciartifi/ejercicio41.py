import os
import pyautogui
import json
import ollama
import time


def conectar_db():
    print("Conectando a PostgreSQL...")
    # Imagina aquí tu lógica de conexión
    return True


def procesar_telemetria_esp32(datos_crudos):
    datos = json.loads(datos_crudos)
    if datos['temperatura'] > 35:
        print("Alerta térmica detectada")
    return datos


def main():
    conectar_db()
    lectura = '{"temperatura": 38, "humedad": 60}'
    procesado = procesar_telemetria_esp32(lectura)
    print("Resultado final:", procesado)


main()
