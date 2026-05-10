import ollama
import json
import time


def mi_funcion_desordenada(parametro1, parametro2):
    resultado = parametro1+parametro2
    print("El resultado es:", resultado)
    if resultado > 10:
        print("Es mayor a 10")
    else:
        print("Es menor o igual")
    return resultado


def otra_funcion():
    datos = {"status": "ok", "valor": 42}
    print(json.dumps(datos))
    return None


otra_funcion()
mi_funcion_desordenada(5,   8)
