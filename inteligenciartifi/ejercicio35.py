import os
import subprocess
import time

# Tu lista de aplicaciones (Asegúrate de que las rutas sean las correctas en tu PC)
APPS = {
    "1": {"nombre": "VS Code (Dev)", "path": "code"}, # 'code' funciona si está en el PATH
    "2": {"nombre": "SQL Server Management", "path": "ssms"},
    "3": {"nombre": "Ollama / Llama 3", "path": "ollama serve"},
    "4": {"nombre": "The House of the Dead", "path": r"C:\Ruta\Al\Juego.exe"}, # Pon tu ruta real
    "5": {"nombre": "TikTok Studio / OBS", "path": "obs"}
}

def menu_interactivo():
    while True:
        # Limpiamos pantalla para que parezca una app independiente
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("======================================")
        print("   🚀 ASPDEV SMART SWITCHER v2.0   ")
        print("======================================")
        print(" Selecciona una herramienta para saltar:")
        print("--------------------------------------")
        
        for k, v in APPS.items():
            print(f" [{k}] -> {v['nombre']}")
            
        print("--------------------------------------")
        print(" [0] -> REGRESAR (Cerrar y volver al CMD)")
        print("======================================")
        
        opcion = input("\n¿A dónde vamos, Mauricio? > ")

        if opcion == "0":
            print("\n🔄 Regresando al sistema original...")
            time.sleep(1)
            break # Rompe el bucle y te devuelve a donde estabas
            
        elif opcion in APPS:
            app = APPS[opcion]
            print(f"✨ Saltando a {app['nombre']}...")
            try:
                # Usamos Popen para que la app se abra y el switcher siga vivo
                subprocess.Popen(app['path'], shell=True)
                print("✅ Ejecutado. El menú se refrescará en 2s.")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Error al abrir: {e}")
                time.sleep(3)
        else:
            print("❗ Opción no válida. Intenta de nuevo.")
            time.sleep(1.5)

if __name__ == "__main__":
    menu_interactivo()