import psutil
import ollama
import os

def matar_procesos_por_perfil():
    print("🛡️  Iniciando Finalizador de Tareas Inteligente...")
    
    # Capturamos procesos que consumen más del 1% de CPU o mucha RAM
    procesos_candidatos = []
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
        try:
            if proc.info['cpu_percent'] > 0.5 or proc.info['memory_info'].rss > 100 * 1024 * 1024: # >100MB
                procesos_candidatos.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    lista_limpia = list(set(procesos_candidatos))
    print(f"🔍 Procesos de alto consumo detectados: {', '.join(lista_limpia[:10])}...")

    # Instrucción para Llama 3
    orden_usuario = input("\n💡 ¿Qué tareas quieres finalizar? (ej: 'todas las apps de ocio', 'todo lo pesado'): ")

    prompt = (
        f"Lista de procesos actuales: {', '.join(lista_limpia)}. "
        f"El usuario quiere: '{orden_usuario}'. "
        "Identifica los ejecutables (.exe) que coinciden con esa orden. "
        "EXCLUYE SIEMPRE: ollama.exe, python.exe, cmd.exe, explorer.exe, taskmgr.exe. "
        "Responde SOLO con los nombres de los archivos .exe separados por comas."
    )

    try:
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
        objetivos = response['message']['content'].strip().split(',')

        print(f"\n⚡ Finalizando las siguientes tareas: {objetivos}")
        
        for exe in objetivos:
            exe = exe.strip()
            if exe and ".exe" in exe.lower():
                # /F = Forzar, /T = Cerrar procesos hijos (árbol de tareas)
                os.system(f"taskkill /f /t /im {exe}")
        
        print("\n✅ Sistema optimizado. Tareas finalizadas con éxito.")

    except Exception as e:
        print(f"❌ Error en la comunicación: {e}")

if __name__ == "__main__":
    matar_procesos_por_perfil()