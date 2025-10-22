import cv2
import numpy as np
import sys
import os

def check_opencv_build():
    """Verifica la construcción de OpenCV y sus capacidades"""
    print("🔍 Información de OpenCV:")
    print(f"   Versión: {cv2.__version__}")
    
    # Verificar backends de video
    print("📹 Backends de video disponibles:")
    backends = []
    for backend in dir(cv2):
        if backend.startswith('CAP_'):
            backends.append(backend)
    
    for backend in backends[:5]:  # Mostrar solo los primeros 5
        print(f"   - {backend}")
    
    return True

def test_camera_with_different_backends():
    """Prueba la cámara con diferentes backends"""
    print("\n🎥 Probando diferentes backends de cámara...")
    
    # Diferentes backends para Windows
    backends_to_try = [
        (cv2.CAP_DSHOW, "DirectShow (Windows)"),
        (cv2.CAP_MSMF, "Media Foundation (Windows)"),  
        (cv2.CAP_ANY, "Automático")
    ]
    
    for backend, name in backends_to_try:
        print(f"\n🔄 Probando {name}...")
        
        try:
            cap = cv2.VideoCapture(0, backend)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"✅ {name} - FUNCIONA!")
                    print(f"   Resolución: {frame.shape}")
                    
                    # Intentar mostrar una ventana de prueba
                    print("   📺 Intentando mostrar ventana...")
                    
                    # Agregar texto al frame
                    cv2.putText(frame, f"Backend: {name}", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, "Presiona cualquier tecla", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    
                    # Crear ventana con configuración específica para Windows
                    window_name = f'Test {name}'
                    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                    cv2.resizeWindow(window_name, 640, 480)
                    cv2.moveWindow(window_name, 100, 100)
                    
                    cv2.imshow(window_name, frame)
                    print(f"   ⏳ Esperando 5 segundos o presiona una tecla...")
                    
                    # Esperar 5 segundos o hasta que se presione una tecla
                    key = cv2.waitKey(5000)
                    
                    cv2.destroyWindow(window_name)
                    cap.release()
                    
                    if key != -1:
                        print(f"   ✅ Tecla detectada: {key}")
                    else:
                        print(f"   ⏰ Tiempo agotado")
                    
                    return True
                else:
                    print(f"❌ {name} - No puede leer frames")
            else:
                print(f"❌ {name} - No puede abrir cámara")
                
            cap.release()
            
        except Exception as e:
            print(f"❌ {name} - Error: {e}")
    
    return False

def check_camera_permissions():
    """Verifica permisos de cámara en Windows"""
    print("\n🔒 Verificando acceso a la cámara...")
    
    # Lista de posibles IDs de cámara
    camera_ids = [0, 1, -1]
    
    for cam_id in camera_ids:
        print(f"   Probando cámara ID {cam_id}...")
        cap = cv2.VideoCapture(cam_id)
        
        if cap.isOpened():
            print(f"   ✅ Cámara {cam_id} accesible")
            cap.release()
        else:
            print(f"   ❌ Cámara {cam_id} no accesible")

def main():
    print("🖥️  DIAGNÓSTICO DE CÁMARA Y OPENCV")
    print("=" * 50)
    
    # Verificar OpenCV
    check_opencv_build()
    
    # Verificar permisos
    check_camera_permissions()
    
    # Probar backends
    success = test_camera_with_different_backends()
    
    if success:
        print("\n🎉 ¡Excelente! OpenCV puede mostrar ventanas y acceder a tu cámara.")
        print("💡 Ahora deberías poder ejecutar la aplicación principal.")
    else:
        print("\n❌ Problemas detectados:")
        print("   1. Verifica que tu cámara web esté conectada")
        print("   2. Cierra otras aplicaciones que usen la cámara (Zoom, Teams, etc.)")
        print("   3. En Windows 10/11, ve a Configuración > Privacidad > Cámara")
        print("      y asegúrate de que las aplicaciones de escritorio puedan acceder")
        print("   4. Intenta ejecutar VS Code como administrador")
    
    print("\n🔄 Presiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()