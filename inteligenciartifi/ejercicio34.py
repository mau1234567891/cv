import psutil
import ollama
import os
import platform

def obtener_datos_hardware():
    # 1. Recolectamos datos crudos del sistema
    uso_cpu = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    temperatura = "No disponible" # Algunos i7 bloquean el acceso directo sin admin
    
    # Intentar obtener info de batería ya que es una laptop
    bateria = psutil.sensors_battery()
    estado_bat = f"{bateria.percent}%" if bateria else "N/A"

    datos = (
        f"Procesador: {platform.processor()}\n"
        f"Uso de CPU: {uso_cpu}%\n"
        f"Memoria RAM: {memoria.percent}% de uso\n"
        f"Espacio en Disco: {disco.percent}% ocupado\n"
        f"Batería: {estado_bat}\n"
    )
    return datos

def diagnostico_ia():
    print("📋 Extrayendo signos vitales de la PC...")
    stats = obtener_datos_hardware()
    
    # 2. Le pasamos los datos a Llama 3 para que los interprete
    prompt = (
        f"Actúa como un experto en hardware. Aquí están los datos de mi laptop:\n\n{stats}\n"
        "Analiza si estos valores son normales para una laptop ASUS con i7. "
        "Si el uso de CPU es alto, recomiéndame qué cerrar. "
        "Sé breve, directo y dime si mi equipo está en peligro de sobrecalentamiento."
    )

    try:
        print("🧠 Llama 3 está revisando el reporte...")
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        
        print("\n" + "="*40)
        print("🩺 DIAGNÓSTICO DEL SISTEMA")
        print("="*40)
        print(response['message']['content'])
        print("="*40)
        
    except Exception as e:
        print(f"❌ Error al conectar con Ollama: {e}")

if __name__ == "__main__":
    diagnostico_ia()