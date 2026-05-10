import psycopg2
import ollama
import time
import requests
from datetime import datetime

# Configuración de Base de Datos
DB_PARAMS = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "12345",
    "port": "5432"
}

SEGUNDOS_ESPERA = 300  # 5 minutos es ideal para no saturar

def obtener_clima_real():
    # Coordenadas de San Salvador (Lat: 13.6894, Lon: -89.1872)
    url = "https://api.open-meteo.com/v1/forecast?latitude=13.6894&longitude=-89.1872&current_weather=true&hourly=relativehumidity_2m"
    try:
        response = requests.get(url)
        data = response.json()
        current = data['current_weather']
        
        # Extraemos los datos reales
        return {
            "temp": current['temperature'],
            "viento": current['windspeed'],
            "condicion_code": current['weathercode'], # Código numérico del clima
            "ciudad": "San Salvador"
        }
    except Exception as e:
        print(f"❌ Error obteniendo clima real: {e}")
        return None

def ejecutar_sistema_autonomo():
    try:
        # 1. Obtener datos reales del mundo
        datos_reales = obtener_clima_real()
        if not datos_reales: return

        # 2. Conexión a Postgres
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # 3. Guardar en BD (Usamos la temperatura real)
        cur.execute("""
            INSERT INTO historial_clima (ciudad, temperatura, condicion)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (datos_reales['ciudad'], datos_reales['temp'], f"Code {datos_reales['condicion_code']}"))
        conn.commit()

        # 4. Obtener historial para la IA
        cur.execute("SELECT fecha, hora, temperatura FROM historial_clima ORDER BY id DESC LIMIT 15;")
        historial = cur.fetchall()
        cur.close()
        conn.close()

        # 5. Inferencia con Llama 3
        print(f"[{datetime.now().strftime('%H:%M:%S')}] IA Procesando datos reales...")
        
        prompt = f"""
        SISTEMA DE DIAGNÓSTICO INDEPENDIENTE
        Ciudad: {datos_reales['ciudad']}
        Temperatura Actual: {datos_reales['temp']}°C
        Velocidad Viento: {datos_reales['viento']} km/h
        Historial reciente: {historial}

        TAREA:
        Como IA soberana, analiza si estos datos reales coinciden con la tendencia. 
        Da un diagnóstico del clima actual en San Salvador y un pronóstico breve.
        """
        
        res = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': 'Eres un meteorólogo digital independiente. No dependes de empresas, solo de datos puros.'},
            {'role': 'user', 'content': prompt}
        ])

        print(f"🤖 RESULTADO IA:\n{res['message']['content']}\n")

    except Exception as e:
        print(f"⚠️ Error: {e}")

# --- INICIO ---
print("🌍 Conectando con satélites de datos abiertos...")
while True:
    ejecutar_sistema_autonomo()
    time.sleep(SEGUNDOS_ESPERA)