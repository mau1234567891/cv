import psycopg2
from psycopg2 import sql
import ollama
from datetime import datetime
import time

# 1. CONFIGURACIÓN DE CONEXIÓN
# Conectamos primero a 'postgres' para poder crear la nueva base de datos
config_inicial = {
    "host": "localhost",
    "user": "postgres",
    "password": "12345",
    "port": "5432"
}
DB_NAME = "db_ia_control"

def iniciar_entorno():
    try:
        # Conexión para crear la DB
        conn = psycopg2.connect(dbname="postgres", **config_inicial)
        conn.autocommit = True
        cur = conn.cursor()

        # Crear Base de Datos
        cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [DB_NAME])
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"[1] Base de datos '{DB_NAME}' creada.")
        else:
            print(f"[1] La base de datos '{DB_NAME}' ya existe.")

        cur.close()
        conn.close()

        # Conexión a la nueva DB para crear la tabla
        conn = psycopg2.connect(dbname=DB_NAME, **config_inicial)
        conn.autocommit = True
        cur = conn.cursor()

        # Crear Tabla
        tabla_sql = """
        CREATE TABLE IF NOT EXISTS registro_inteligente (
            id SERIAL PRIMARY KEY,
            modulo TEXT,
            valor_sensor NUMERIC,
            interpretacion_ia TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(tabla_sql)
        print("[2] Tabla 'registro_inteligente' lista.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error en configuración: {e}")

def generar_y_almacenar():
    """Llama 3 genera un dato y lo guardamos en Postgres."""
    try:
        # Pedimos a Llama 3 un dato simulado y un análisis
        prompt = "Genera un valor de temperatura para un motor (entre 20 y 100) y una breve conclusión de 5 palabras. Formato: valor|conclusion"
        response = ollama.generate(model='llama3', prompt=prompt)
        output = response['response'].strip()
        
        # Procesamos la respuesta de la IA
        valor, conclusion = output.split('|')

        # Guardar en PostgreSQL
        conn = psycopg2.connect(dbname=DB_NAME, **config_inicial)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO registro_inteligente (modulo, valor_sensor, interpretacion_ia) VALUES (%s, %s, %s)",
            ("Motor_Principal", float(valor), conclusion)
        )
        conn.commit()
        print(f"-> Guardado: {valor}°C | IA: {conclusion}")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error al procesar con IA: {e}")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    iniciar_entorno()
    print("\n[3] Iniciando almacenamiento en tiempo real con Llama 3...")
    while True:
        generar_y_almacenar()
        time.sleep(5) # Pausa de 5 segundos entre registros