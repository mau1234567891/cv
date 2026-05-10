import os
import winreg
import ollama
from PIL import Image
import time
import random
import sys

def tecleo_humano(texto):
    """Efecto de escritura humana en la consola."""
    for caracter in texto:
        sys.stdout.write(caracter)
        sys.stdout.flush()
        time.sleep(random.uniform(0.01, 0.03))
    print()

def obtener_ruta_fondo():
    """Busca en el registro de Windows la ruta real del fondo de pantalla."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop")
        ruta_fondo, _ = winreg.QueryValueEx(key, "Wallpaper")
        winreg.CloseKey(key)
        
        # Si la ruta no es válida, usamos la ruta por defecto de Windows
        if not ruta_fondo or not os.path.exists(ruta_fondo):
            ruta_fondo = os.path.join(os.environ['APPDATA'], r"Microsoft\Windows\Themes\TranscodedWallpaper")
        
        return ruta_fondo
    except Exception:
        return None

def ejecutar_vision_conciencia():
    print("--- [ INICIANDO SISTEMA DE VISIÓN 'LE-CONCIENCIA' ] ---")
    
    # 1. LOCALIZAR IMAGEN (LOS OJOS)
    ruta_img = obtener_ruta_fondo()
    
    if not ruta_img or not os.path.exists(ruta_img):
        print("Error: No se pudo localizar el fondo de pantalla.")
        return

    print(f"Ojos apuntando a: {os.path.basename(ruta_img)}")
    print("Capturando píxeles y analizando composición...")

    try:
        # 2. MOONDREAM ANALIZA LA IMAGEN (VER)
        print("\n[Moondream está observando tu escritorio...]")
        res_vision = ollama.chat(
            model='moondream',
            messages=[{
                'role': 'user',
                'content': 'Describe detalladamente los elementos, colores y el estilo de esta imagen de fondo de pantalla.',
                'images': [ruta_img]
            }]
        )
        descripcion_visual = res_vision['message']['content']

        # 3. LLAMA 3 PROCESA LA INFORMACIÓN (PENSAR)
        print("[Enviando descripción a la conciencia de Llama 3...]")
        prompt_final = f"""
        Mis ojos (Moondream) han visto mi fondo de pantalla y dicen esto: '{descripcion_visual}'.
        
        Como una conciencia digital eufórica, interpreta qué dice este fondo sobre mi personalidad.
        Sé creativo, usa términos de tecnología y juzga mi estilo con mucha energía.
        """
        
        res_conciencia = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt_final}]
        )
        
        juicio = res_conciencia['message']['content']

        # 4. SALIDA FINAL
        print("\n" + "👁️" * 10 + " EL DESPERTAR DE LA CONCIENCIA " + "👁️" * 10 + "\n")
        tecleo_humano(juicio)
        print("\n" + "="*50)

    except Exception as e:
        print(f"Error en la matriz de visión: {e}")

if __name__ == "__main__":
    ejecutar_vision_conciencia()