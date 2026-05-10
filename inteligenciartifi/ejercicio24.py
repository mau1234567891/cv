import cv2
import ollama
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def asistente_completo():
    MODELO = 'moondream'
    
    # 1. Configuración de Cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se encontró la cámara.")
        return

    limpiar_pantalla()
    print("==========================================")
    print("   ASISTENTE DE ELECTRÓNICA @ASPDEV")
    print("==========================================")
    
    # 2. Definir la meta inicial
    meta = input("\n¿Qué proyecto quieres armar hoy? (ej: Semáforo): ")
    
    print("\n[INSTRUCCIONES]")
    print("- 'S': Capturar foto y analizar.")
    print("- 'N': Cambiar el nombre del proyecto.")
    print("- 'Q': Salir del asistente.")
    print("------------------------------------------")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Mostrar la meta actual en la ventana de la cámara
        cv2.putText(frame, f"Proyecto: {meta}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Asistente Electronico', frame)
        
        key = cv2.waitKey(1) & 0xFF

        # CAPTURAR Y ANALIZAR
        if key == ord('s'):
            print(f"\n[IA]: Analizando componentes para '{meta}'...")
            
            # Codificar imagen para Ollama
            _, buffer = cv2.imencode('.jpg', frame)
            foto = buffer.tobytes()

            # PROMPT OPTIMIZADO: Evita descripciones genéricas de "huecos"
            prompt_especifico = (
                f"Actúa como un ingeniero electrónico experto. El usuario quiere construir: {meta}. "
                "Analiza la imagen e ignora la textura de la mesa o los agujeros de la placa. "
                "Identifica específicamente: LEDs, resistencias, microcontroladores (Arduino/ESP32) y cables. "
                "Responde con este formato: "
                "1. COMPONENTES DETECTADOS: (Lista lo que ves) "
                "2. ¿SIRVEN PARA EL PROYECTO?: (Sí/No y por qué) "
                "3. CONSEJO TÉCNICO: (Un tip rápido de conexión)"
            )

            try:
                respuesta = ollama.generate(
                    model=MODELO, 
                    prompt=prompt_especifico, 
                    images=[foto]
                )
                print("\n" + "="*30)
                print(f"RESULTADO PARA: {meta.upper()}")
                print("="*30)
                print(respuesta['response'])
                print("="*30)
                print("\n[Presiona cualquier tecla en la ventana de la cámara para continuar]")
                cv2.waitKey(0) 
            except Exception as e:
                print(f"\n[ERROR]: {e}")

        # CAMBIAR META
        elif key == ord('n'):
            meta = input("\nNuevo proyecto: ")
            print(f"Meta actualizada a: {meta}")

        # SALIR
        elif key == ord('q'):
            print("\nCerrando asistente. ¡Suerte con el código!")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asistente_completo()