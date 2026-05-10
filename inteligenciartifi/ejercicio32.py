import winreg
import os
import subprocess
import shutil

def refrescar_explorer():
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True)
    subprocess.run(["start", "explorer.exe"], shell=True)

def gestionar_extensiones(mostrar=True):
    ruta = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
    valor = 0 if mostrar else 1 # 0 es mostrar, 1 es ocultar
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, ruta, 0, winreg.KEY_ALL_ACCESS) as key:
        winreg.SetValueEx(key, "HideFileExt", 0, winreg.REG_DWORD, valor)
    print(f"✅ Extensiones {'Visibles' if mostrar else 'Ocultas'}.")

def gestionar_ocultos(mostrar=True):
    ruta = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
    valor = 1 if mostrar else 2 # 1 es mostrar, 2 es no mostrar
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, ruta, 0, winreg.KEY_ALL_ACCESS) as key:
        winreg.SetValueEx(key, "Hidden", 0, winreg.REG_DWORD, valor)
    print(f"✅ Archivos ocultos {'Visibles' if mostrar else 'Ocultos'}.")

def ordenar_archivos_por_tipo():
    # Ordena la carpeta actual o una específica
    ruta = input("📁 Ingresa la ruta de la carpeta a ordenar (o presiona Enter para esta): ") or "."
    for archivo in os.listdir(ruta):
        if os.path.isfile(os.path.join(ruta, archivo)):
            ext = archivo.split('.')[-1].lower() if '.' in archivo else 'otros'
            carpeta_destino = os.path.join(ruta, ext.upper())
            
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)
            
            shutil.move(os.path.join(ruta, archivo), os.path.join(carpeta_destino, archivo))
    print(f"✅ Archivos ordenados por extensión en carpetas separadas.")

def menu_dominio():
    while True:
        print("\n--- 🕹️ MENU DE DOMINIO DE ARCHIVOS ---")
        print("1. Mostrar extensiones (.py, .txt)")
        print("2. Ocultar extensiones")
        print("3. Mostrar archivos ocultos")
        print("4. Ocultar archivos ocultos")
        print("5. Ordenar archivos por tipo (Crear carpetas)")
        print("6. Refrescar Explorador (Aplicar cambios)")
        print("0. Salir")
        
        opcion = input("\nElige una opción: ")

        if opcion == "1": gestionar_extensiones(True)
        elif opcion == "2": gestionar_extensiones(False)
        elif opcion == "3": gestionar_ocultos(True)
        elif opcion == "4": gestionar_ocultos(False)
        elif opcion == "5": ordenar_archivos_por_tipo()
        elif opcion == "6": refrescar_explorer()
        elif opcion == "0": break
        else: print("❌ Opción no válida.")

if __name__ == "__main__":
    menu_dominio()