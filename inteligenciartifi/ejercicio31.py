import winreg
import os

def cambiar_visibilidad_extensiones():
    # Ruta en el registro donde Windows guarda esta configuración
    ruta_registro = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
    nombre_valor = "HideFileExt"

    try:
        # 1. Abrimos la "llave" del registro para leer y escribir
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, ruta_registro, 0, winreg.KEY_ALL_ACCESS) as key:
            # 2. Leemos el estado actual
            # 1 = Ocultas, 0 = Visibles
            valor_actual, _ = winreg.QueryValueEx(key, nombre_valor)

            # 3. Switcheamos el valor
            nuevo_valor = 0 if valor_actual == 1 else 1
            winreg.SetValueEx(key, nombre_valor, 0, winreg.REG_DWORD, nuevo_valor)

            # 4. Mensaje de estado
            estado = "VISIBLES" if nuevo_valor == 0 else "OCULTAS"
            print(f"✅ Dominio del Sistema: Las extensiones ahora están {estado}.")
            
            # 5. Forzamos al Explorador a refrescarse para ver el cambio
            import subprocess
            subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True)
            subprocess.run(["start", "explorer.exe"], shell=True)
            print("🔄 Explorador de archivos reiniciado para aplicar cambios.")

    except Exception as e:
        print(f"❌ Error de permisos: {e}")
        print("💡 Consejo: Ejecuta el script o VS Code como ADMINISTRADOR.")

if __name__ == "__main__":
    cambiar_visibilidad_extensiones()