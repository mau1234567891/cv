import cv2
import ollama

def asistente_solo_moondream():
    MODELO = 'moondream'
    cap = cv2.VideoCapture(0)
    
    print(f"--- MODO LIGERO: {MODELO.upper()} ---")
    print("Presiona 's' para analizar | 'q' para salir")

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        cv2.imshow('Camara - Solo Moondream', frame)
        key = cv2.waitKey(1)
        
        if key & 0xFF == ord('s'):
            _, buffer = cv2.imencode('.jpg', frame)
            foto = buffer.tobytes()
            
            print("\n[IA]: Analizando imagen directamente...")
            try:
                # Al usar solo un modelo, la respuesta es mucho más rápida
                res = ollama.generate(
                    model=MODELO,
                    prompt="Describe detalladamente los componentes electrónicos que ves. Si hay errores de conexión o componentes mal puestos, menciónalo.",
                    images=[foto]
                )
                print(f"\n--- ANÁLISIS ---\n{res['response']}")
                
            except Exception as e:
                print(f"Error: {e}")

        elif key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asistente_solo_moondream()