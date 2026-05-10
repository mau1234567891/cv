import pymongo
import os
import sys
from bson.json_util import dumps

# CONFIGURACIÓN (Usa tus datos de Atlas)
URI = "mongodb+srv://mauricioalexander27121999:khHHtiELxLC85Q6@cluster0.l7i0y.mongodb.net/?appName=Cluster0"
DB_NAME = "ia12"          
COL_NAME = "Index"     

def iniciar_controlador():
    try:
        client = pymongo.MongoClient(URI)
        db = client[DB_NAME]
        coleccion = db[COL_NAME]
        
        print(f"\n--- CONTROLADOR REMOTO ACTIVO EN POWERSHELL ---")
        print(f"Esperando comandos desde MongoDB...\n")

        # Escuchando inserciones en tiempo real
        with coleccion.watch() as stream:
            for cambio in stream:
                if cambio['operationType'] == "insert":
                    # Extraemos el comando del documento
                    documento = cambio['fullDocument']
                    comando = documento.get('comando_puro')

                    if comando:
                        print(f"[*] Recibido: {comando}")
                        print(f"[*] Ejecutando...")
                        
                        # ESTA LÍNEA EJECUTA EL COMANDO EN TU PC
                        os.system(comando)
                        
                        print(f"[OK] Comando procesado.\n")
                        print("-" * 40)

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    iniciar_controlador()