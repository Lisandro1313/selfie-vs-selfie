import cv2
import numpy as np
from hand_detector import HandDetector
from gesture_recognizer import GestureRecognizer
from utils import FPSCounter, draw_text_with_outline


def debug_scissors():
    """
    Modo de depuración específico para el gesto de tijeras.
    """
    print("🔍 MODO DEBUG: Detección de Tijeras")
    print("=====================================")
    print("Instrucciones:")
    print("1. Haz el gesto de tijeras (índice y medio extendidos)")
    print("2. Observa la información de debug en pantalla")
    print("3. Presiona 'q' para salir")
    print()
    
    # Inicializar componentes
    hand_detector = HandDetector(max_num_hands=1, min_detection_confidence=0.7)
    gesture_recognizer = GestureRecognizer()
    fps_counter = FPSCounter()
    
    # Inicializar cámara
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    cv2.namedWindow('Debug Tijeras', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Debug Tijeras', 800, 600)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        
        # Detectar manos
        frame, hands_data = hand_detector.detect_hands(frame, draw=True)
        
        # Actualizar FPS
        fps = fps_counter.update()
        fps_counter.draw_fps(frame, fps)
        
        if hands_data:
            landmarks = hands_data[0]['landmarks']
            
            # Obtener información detallada
            fingers_up, finger_status = gesture_recognizer.count_fingers(landmarks)
            rps_gesture = gesture_recognizer.recognize_rock_paper_scissors(landmarks)
            
            # Debug específico para tijeras
            debug_scissors_info(frame, landmarks, finger_status, rps_gesture, gesture_recognizer)
        else:
            draw_text_with_outline(frame, "NO SE DETECTA MANO", 
                                  (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow('Debug Tijeras', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()


def debug_scissors_info(frame, landmarks, finger_status, rps_gesture, gesture_recognizer):
    """
    Muestra información detallada de debug para tijeras.
    """
    y_offset = 80
    line_height = 25
    
    # Crear fondo para debug info
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 70), (500, 400), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # Título
    draw_text_with_outline(frame, "DEBUG TIJERAS", 
                          (20, y_offset), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 0), 2)
    y_offset += 30
    
    # Estado de cada dedo
    finger_names = ["Pulgar", "Indice", "Medio", "Anular", "Meñique"]
    for i, (name, is_up) in enumerate(zip(finger_names, finger_status)):
        color = (0, 255, 0) if is_up else (0, 0, 255)
        status = "UP" if is_up else "DOWN"
        draw_text_with_outline(frame, f"{name}: {status}", 
                              (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        y_offset += line_height
    
    # Resultado RPS
    y_offset += 10
    rps_color = (0, 255, 0) if rps_gesture == "scissors" else (0, 0, 255)
    draw_text_with_outline(frame, f"RPS Detectado: {rps_gesture.upper()}", 
                          (20, y_offset), cv2.FONT_HERSHEY_DUPLEX, 0.6, rps_color, 2)
    y_offset += 30
    
    # Análisis específico de tijeras
    if len(landmarks) >= 21:
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        palm_y = landmarks[9][1]
        
        # Calcular distancias y posiciones
        distance_index_middle = np.sqrt((index_tip[0] - middle_tip[0])**2 + 
                                       (index_tip[1] - middle_tip[1])**2)
        
        index_extended = index_tip[1] < palm_y - 20
        middle_extended = middle_tip[1] < palm_y - 20
        ring_folded = ring_tip[1] > palm_y - 30
        pinky_folded = pinky_tip[1] > palm_y - 30
        fingers_separated = distance_index_middle > 25
        
        # Mostrar criterios
        draw_text_with_outline(frame, "CRITERIOS TIJERAS:", 
                              (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        y_offset += 20
        
        criteria = [
            ("Indice extendido", index_extended),
            ("Medio extendido", middle_extended), 
            ("Anular doblado", ring_folded),
            ("Meñique doblado", pinky_folded),
            ("Dedos separados", fingers_separated),
            (f"Distancia: {distance_index_middle:.1f}", distance_index_middle > 25)
        ]
        
        for criterion, passed in criteria:
            color = (0, 255, 0) if passed else (0, 0, 255)
            status = "✓" if passed else "✗"
            draw_text_with_outline(frame, f"{status} {criterion}", 
                                  (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            y_offset += 18
        
        # Dibujar puntos clave
        cv2.circle(frame, tuple(index_tip), 8, (255, 0, 0), -1)
        cv2.circle(frame, tuple(middle_tip), 8, (0, 255, 0), -1)
        cv2.circle(frame, tuple(ring_tip), 8, (0, 0, 255), -1)
        cv2.circle(frame, tuple(pinky_tip), 8, (255, 0, 255), -1)
        
        # Línea entre índice y medio
        cv2.line(frame, tuple(index_tip), tuple(middle_tip), (255, 255, 0), 2)
    
    # Instrucciones
    draw_text_with_outline(frame, "Haz gesto de TIJERAS", 
                          (20, frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    draw_text_with_outline(frame, "Presiona 'q' para salir", 
                          (20, frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


if __name__ == "__main__":
    debug_scissors()