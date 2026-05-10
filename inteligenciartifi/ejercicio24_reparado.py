```
import cv2
import ollama
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def electronic_assistant():
    MODEL_NAME = 'moondream'

    camera_cap = cv2.VideoCapture(0)
    if not camera_cap.isOpened():
        print("Error: Camera not found.")
        return

    clear_screen()
    print("==========================================")
    print(f"ASISTENTE DE ELECTRÓNICA @ASPDEV {camera_cap.get(3)}x{camera_cap.get(4)}")
    print("==========================================")

    initial_project = input("\nWhat project do you want to build today? (e.g. Semáforo): ")

    print("\n[INSTRUCTIONS]")
    print("- 'S': Capture photo and analyze.")
    print("- 'N': Change project name.")
    print("- 'Q': Exit the assistant.")
    print("------------------------------------------")

    while True:
        ret, frame = camera_cap.read()
        if not ret:
            break

        cv2.putText(frame, f"Project: {initial_project}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Electronic Assistant', frame)
        
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            print(f"\n[AI]: Analyzing components for '{initial_project}'...")
            
            _, buffer = cv2.imencode('.jpg', frame)
            foto = buffer.tobytes()

            prompt_optimized = (
                f"Act like an expert electronics engineer. The user wants to build: {initial_project}. "
                "Analyze the image and ignore the texture of the desk or holes in the PCB. "
                "Identify specifically: LEDs, resistances, microcontrollers (Arduino/ESP32) and cables. "
                "Respond with this format: "
                "1. DETECTED COMPONENTS: (List what you see) "
                "2. DO THEY SERVE THE PROJECT?: (Yes/No and why) "
                "3. TECHNICAL TIP: (A quick connection tip)"
            )

            try:
                response = ollama.generate(
                    model=MODEL_NAME, 
                    prompt=prompt_optimized, 
                    images=[foto]
                )
                print("\n" + "="*30)
                print(f"RESULT FOR: {initial_project.upper()}")
                print("="*30)
                print(response['response'])
                print("="*30)
                print("\n[Press any key in the camera window to continue]")
                cv2.waitKey(0) 
            except Exception as e:
                print(f"\n[ERROR]: {e}")

        elif key == ord('n'):
            initial_project = input("\nNew project: ")
            print(f"Project updated to: {initial_project}")

        elif key == ord('q'):
            print("\nClosing assistant. Good luck with the code!")
            break

    camera_cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    electronic_assistant()