import sys
import os
import pkg_resources # Para ver versiones

def auditar_librerias_activas():
    print("\n🔍 AUDITORÍA DE LIBRERÍAS EN TIEMPO REAL")
    print("="*50)
    
    # sys.modules contiene todos los módulos cargados en la sesión actual
    modulos_cargados = sys.modules.copy()
    
    contador = 0
    print(f"{'LIBRERÍA':<25} | {'ORIGEN':<30}")
    print("-" * 60)

    for nombre, modulo in modulos_cargados.items():
        # Filtramos solo las librerías principales (no los sub-módulos internos)
        if "." not in nombre:
            try:
                # Intentamos obtener la ruta del archivo de la librería
                ruta = getattr(modulo, '__file__', 'Integrada (Built-in)')
                
                # Intentamos obtener la versión si está disponible
                try:
                    version = pkg_resources.get_distribution(nombre).version
                except:
                    version = "N/A"

                print(f"{nombre:<15} ({version:<7}) | {ruta[:40]}...")
                contador += 1
            except Exception:
                continue

    print("-" * 60)
    print(f"✅ Auditoría completa: {contador} librerías principales detectadas en memoria.")
    print("💡 Estas son las librerías que están consumiendo recursos de tu Ryzen 7 ahora mismo.")

if __name__ == "__main__":
    # Importamos algo pesado solo para probar el monitor
    print("Cargando entorno de prueba...")
    import json
    import sqlite3
    
    auditar_librerias_activas()