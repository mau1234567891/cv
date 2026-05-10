import ollama
import pyautogui
import time

def inyectar_dashboard_colab():
    # Contexto para generar un reporte visualmente impactante
    prompt_ingeniero = (
        "Eres un experto en frontend y sistemas embebidos. "
        "Genera un código HTML único y moderno (usando estilos en línea/inline CSS) "
        "para un dashboard que resuma estos logros: "
        "1. Biometría MAX30102 activa. 2. Visión Moondream integrada. 3. SQL Sync OK. "
        "Usa colores oscuros, neones verdes y animaciones simples. "
        "IMPORTANTE: Solo entrega el código HTML, sin explicaciones."
    )
    
    print("🚀 Llama 3 diseñando el dashboard de ingeniería...")
    
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': prompt_ingeniero},
            {'role': 'user', 'content': "Crea el HTML para mostrar mis avances de forma épica."},
        ])

        codigo_html = response['message']['content'].strip()
        
        # Preparar el comando para Google Colab
        # Colab necesita la función IPython.display para renderizar HTML
        script_colab = f"""
from IPython.display import HTML
display(HTML('''
{codigo_html}
'''))
"""
        
        print("\n⚠️ PREPARADO: Haz clic en una celda de código en Colab...")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        # Escribir el bloque de código completo
        pyautogui.write(script_colab, interval=0.001)
        
        # Ejecutar celda
        pyautogui.hotkey('ctrl', 'enter')
        print("\n✅ Dashboard inyectado y ejecutado.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inyectar_dashboard_colab()