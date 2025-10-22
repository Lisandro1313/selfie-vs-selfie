import cv2
import time

def simple_camera_test():
    """
    Prueba simple de cámara que definitivamente debe mostrar una ventana.
    """
    print("🎥 Iniciando prueba simple de cámara...")
    
    # Abrir cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        return
    
    print("✅ Cámara abierta exitosamente")
    print("📺 Presiona 'q' para salir")
    
    # Crear ventana explícitamente
    cv2.namedWindow('Prueba Camara Simple', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Prueba Camara Simple', 800, 600)
    
    frame_count = 0
    
    while True:
        # Leer frame
        ret, frame = cap.read()
        
        if not ret:
            print("❌ No se pudo leer frame")
            break
        
        frame_count += 1
        
        # Voltear horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Agregar texto
        cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "Presiona 'q' para salir", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Mostrar frame
        cv2.imshow('Prueba Camara Simple', frame)
        
        # Verificar teclas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # 'q' o ESC
            break
        
        # Log cada 60 frames
        if frame_count % 60 == 0:
            print(f"📊 Frames mostrados: {frame_count}")
    
    # Limpiar
    cap.release()
    cv2.destroyAllWindows()
    print("🧹 Cámara cerrada")

if __name__ == "__main__":
    simple_camera_test()