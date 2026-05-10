import ollama
import os

def auditor_de_codigo():
    print("\n--- [ AGENTE DE AUDITORÍA DE CÓDIGO .PY ] ---")
    
    archivo_py = input("Nombre del script Python a auditar: ")

    if not os.path.exists(archivo_py):
        print(f"❌ El archivo '{archivo_py}' no existe.")
        return

    try:
        with open(archivo_py, 'r', encoding='utf-8') as f:
            codigo = f.read()

        print(f"🛡️ Analizando lógica de seguridad en '{archivo_py}'...")

        # Prompt especializado en ciberseguridad de software
        prompt_auditoria = f"""
        Actúa como un experto en Ciberseguridad y Auditoría de Código.
        Analiza el siguiente script de Python en busca de:
        1. Credenciales expuestas (API Keys, contraseñas, tokens).
        2. Vulnerabilidades de inyección (SQL, Command Injection).
        3. Uso de funciones peligrosas (eval(), exec(), os.system() sin validar).
        4. Fugas de datos o mala gestión de archivos.

        CÓDIGO:
        \"\"\"
        {codigo}
        \"\"\"

        RESPUESTA:
        - Si es SEGURO o tiene RIESGOS.
        - Detalla cada vulnerabilidad encontrada.
        - Sugiere el código corregido para mitigar el riesgo.
        """

        respuesta = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt_auditoria}]
        )

        print("\n" + "🐍" * 15)
        print(f"REPORTE TÉCNICO PARA: {archivo_py}")
        print(respuesta['message']['content'])
        print("🐍" * 15)

    except Exception as e:
        print(f"Error al auditar el código: {e}")

if __name__ == "__main__":
    auditor_de_codigo()