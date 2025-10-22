import cv2
import sys

def test_camera():
    """
    Prueba simple para verificar si la cámara funciona.
    """
    print("🔍 Probando acceso a la cámara...")
    
    # Intentar diferentes IDs de cámara
    camera_ids = [0, 1, 2]
    
    for camera_id in camera_ids:
        print(f"Intentando cámara ID: {camera_id}")
        cap = cv2.VideoCapture(camera_id)
        
        if cap.isOpened():
            print(f"✅ Cámara {camera_id} encontrada!")
            
            # Leer un frame de prueba
            ret, frame = cap.read()
            if ret:
                print(f"✅ Frame capturado exitosamente: {frame.shape}")
                
                # Mostrar ventana de prueba
                cv2.imshow(f'Prueba Camara {camera_id}', frame)
                print("📺 Ventana de prueba abierta. Presiona cualquier tecla para continuar...")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                cap.release()
                return camera_id
            else:
                print(f"❌ No se pudo leer frame de cámara {camera_id}")
        else:
            print(f"❌ No se pudo abrir cámara {camera_id}")
        
        cap.release()
    
    print("❌ No se encontró ninguna cámara funcional")
    return None

if __name__ == "__main__":
    working_camera = test_camera()
    
    if working_camera is not None:
        print(f"\n🎉 Cámara funcional encontrada: ID {working_camera}")
        print("✅ OpenCV puede acceder a tu cámara correctamente")
        
        # Probar que las ventanas de OpenCV funcionen
        print("\n🪟 Probando ventanas de OpenCV...")
        test_window = cv2.Mat.zeros(300, 400, cv2.CV_8UC3)
        cv2.putText(test_window, "Prueba OpenCV", (50, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Prueba Ventana", test_window)
        print("📺 Si ves esta ventana, presiona cualquier tecla...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    else:
        print("\n❌ Problemas encontrados:")
        print("1. No se puede acceder a la cámara")
        print("2. Verifica que:")
        print("   - La cámara esté conectada")
        print("   - No esté siendo usada por otra aplicación")
        print("   - Windows tenga permisos de cámara para Python")