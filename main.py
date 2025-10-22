import cv2
import numpy as np
from hand_detector import HandDetector
from gesture_recognizer import GestureRecognizer
from utils import FPSCounter, draw_gesture_info, draw_controls_info, save_screenshot


class HandGestureApp:
    def __init__(self):
        """
        Inicializa la aplicación de reconocimiento de gestos de mano.
        """
        # Inicializar componentes
        self.hand_detector = HandDetector(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.gesture_recognizer = GestureRecognizer()
        self.fps_counter = FPSCounter()
        
        # Variables de estado
        self.cap = None
        self.running = False
        self.show_landmarks = True
        self.screenshot_counter = 0
        
        # Modos de visualización
        self.display_modes = ["Normal", "RPS", "Contador", "Completo"]
        self.current_mode = 0
        
        print("🖐️ Hand Gesture Recognition App Inicializada")
        print("Controles:")
        print("  ESC/Q: Salir")
        print("  C: Cambiar modo de visualización")
        print("  R: Reiniciar contador de capturas")
        print("  S: Guardar captura de pantalla")
        print("  L: Mostrar/ocultar landmarks")
    
    def initialize_camera(self, camera_id=0):
        """
        Inicializa la cámara.
        
        Args:
            camera_id: ID de la cámara (0 por defecto)
            
        Returns:
            success: True si la cámara se inicializó correctamente
        """
        # Usar DirectShow backend que sabemos que funciona en Windows
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        
        if not self.cap.isOpened():
            print(f"❌ Error: No se pudo abrir la cámara {camera_id}")
            return False
        
        # Configurar resolución más baja para mejor rendimiento
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Verificar configuración
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        print(f"✅ Cámara inicializada: {width}x{height} @ {fps} FPS")
        
        # Probar captura de frame
        ret, test_frame = self.cap.read()
        if not ret:
            print("❌ Error: No se puede leer frames de la cámara")
            return False
        
        print(f"✅ Frame de prueba capturado: {test_frame.shape}")
        return True
    
    def process_frame(self, frame):
        """
        Procesa un frame de video para detectar manos y gestos.
        
        Args:
            frame: Frame de video
            
        Returns:
            processed_frame: Frame procesado con información de gestos
            hands_info: Lista con información de las manos detectadas
        """
        # Voltear horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Detectar manos
        frame, hands_data = self.hand_detector.detect_hands(
            frame, draw=self.show_landmarks
        )
        
        hands_info = []
        
        # Procesar cada mano detectada
        for hand_data in hands_data:
            landmarks = hand_data['landmarks']
            gesture_info = self.gesture_recognizer.get_gesture_info(landmarks)
            
            hand_info = {
                'landmarks': landmarks,
                'label': hand_data['label'],
                'score': hand_data['score'],
                'gesture': gesture_info
            }
            hands_info.append(hand_info)
        
        return frame, hands_info
    
    def draw_interface(self, frame, hands_info, fps):
        """
        Dibuja la interfaz de usuario en el frame.
        
        Args:
            frame: Frame de video
            hands_info: Lista con información de las manos
            fps: FPS actual
        """
        # Dibujar FPS
        self.fps_counter.draw_fps(frame, fps)
        
        # Dibujar información de controles
        draw_controls_info(frame)
        
        # Dibujar modo actual
        mode_text = f"Modo: {self.display_modes[self.current_mode]}"
        cv2.putText(frame, mode_text, (10, frame.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        # Dibujar información de gestos según el modo
        if hands_info:
            self.draw_gesture_interface(frame, hands_info)
    
    def draw_gesture_interface(self, frame, hands_info):
        """
        Dibuja la interfaz específica de gestos según el modo actual.
        
        Args:
            frame: Frame de video
            hands_info: Lista con información de las manos
        """
        for i, hand_info in enumerate(hands_info):
            gesture_info = hand_info['gesture']
            hand_label = hand_info['label']
            
            # Posición base para cada mano
            base_x = 10 if hand_label == "Left" else frame.shape[1] - 400
            base_y = 70 + i * 200
            
            if self.current_mode == 0:  # Normal
                draw_gesture_info(frame, gesture_info, (base_x, base_y))
            
            elif self.current_mode == 1:  # RPS
                self.draw_rps_mode(frame, gesture_info, (base_x, base_y))
            
            elif self.current_mode == 2:  # Contador
                self.draw_counter_mode(frame, gesture_info, (base_x, base_y))
            
            elif self.current_mode == 3:  # Completo
                self.draw_complete_mode(frame, gesture_info, (base_x, base_y))
    
    def draw_rps_mode(self, frame, gesture_info, position):
        """
        Dibuja interfaz específica para Piedra, Papel, Tijeras.
        """
        x, y = position
        
        # Crear fondo para mejor visibilidad
        overlay = frame.copy()
        cv2.rectangle(overlay, (x-10, y-40), (x+400, y+120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Título con contorno
        from utils import draw_text_with_outline
        draw_text_with_outline(frame, "PIEDRA PAPEL TIJERAS", 
                              (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 255), 2)
        
        # Gesto actual con tamaño más grande
        rps_name = gesture_info['rps_name'].replace("🗿", "").replace("📄", "").replace("✂️", "").replace("❓", "").strip()
        color = (0, 255, 0) if gesture_info['rps_gesture'] != "unknown" else (0, 0, 255)
        draw_text_with_outline(frame, rps_name.upper(), 
                              (x, y + 60), cv2.FONT_HERSHEY_DUPLEX, 1.5, color, 3)
    
    def draw_counter_mode(self, frame, gesture_info, position):
        """
        Dibuja interfaz específica para contar dedos con mejor visibilidad.
        """
        x, y = position
        
        # Crear fondo para mejor visibilidad
        overlay = frame.copy()
        cv2.rectangle(overlay, (x-10, y-40), (x+300, y+180), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Título con contorno
        from utils import draw_text_with_outline
        draw_text_with_outline(frame, "CONTADOR DE DEDOS", 
                              (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 0), 2)
        
        # Número grande con contorno
        fingers_count = gesture_info['fingers_count']
        draw_text_with_outline(frame, str(fingers_count), 
                              (x + 80, y + 80), cv2.FONT_HERSHEY_DUPLEX, 4, (0, 255, 0), 6)
        
        # Estado de dedos con nombres claros
        finger_names = ["PULGAR", "INDICE", "MEDIO", "ANULAR", "MEÑIQUE"]
        finger_status = gesture_info['finger_status']
        
        for i, (name, is_up) in enumerate(zip(finger_names, finger_status)):
            color = (0, 255, 0) if is_up else (100, 100, 100)
            status_text = "✓" if is_up else "✗"
            
            # Mostrar solo los primeros 3 dedos para no saturar
            if i < 3:
                draw_text_with_outline(frame, f"{name[:3]}: {status_text}", 
                                      (x, y + 120 + i * 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 1)
    
    def draw_complete_mode(self, frame, gesture_info, position):
        """
        Dibuja interfaz completa con toda la información.
        """
        x, y = position
        line_height = 25
        
        # Información básica
        cv2.putText(frame, f"Dedos: {gesture_info['fingers_count']}/5", 
                   (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.putText(frame, f"RPS: {gesture_info['rps_name']}", 
                   (x, y + line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Gestos especiales
        if gesture_info['is_pointing']:
            cv2.putText(frame, f"➡️ {gesture_info['point_direction']}", 
                       (x, y + 2*line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        
        if gesture_info['thumbs_gesture']:
            emoji = "👍" if gesture_info['thumbs_gesture'] == "thumbs_up" else "👎"
            cv2.putText(frame, f"Pulgar: {emoji}", 
                       (x, y + 3*line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        if gesture_info['is_peace_sign']:
            cv2.putText(frame, "✌️ Paz", 
                       (x, y + 4*line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    def handle_keyboard_input(self, key, frame, hands_info):
        """
        Maneja la entrada del teclado.
        
        Args:
            key: Tecla presionada
            frame: Frame actual
            hands_info: Información de las manos
            
        Returns:
            continue_running: True para continuar, False para salir
        """
        # Salir
        if key in [27, ord('q'), ord('Q')]:  # ESC o Q
            return False
        
        # Cambiar modo
        elif key in [ord('c'), ord('C')]:
            self.current_mode = (self.current_mode + 1) % len(self.display_modes)
            print(f"🔄 Modo cambiado a: {self.display_modes[self.current_mode]}")
        
        # Reiniciar contador
        elif key in [ord('r'), ord('R')]:
            self.screenshot_counter = 0
            print("🔄 Contador de capturas reiniciado")
        
        # Guardar captura
        elif key in [ord('s'), ord('S')]:
            if hands_info:
                self.screenshot_counter += 1
                gesture_info = hands_info[0]['gesture']  # Primera mano
                filename = save_screenshot(frame, gesture_info, self.screenshot_counter)
                print(f"📸 Captura guardada: {filename}")
            else:
                print("⚠️ No hay manos detectadas para capturar")
        
        # Mostrar/ocultar landmarks
        elif key in [ord('l'), ord('L')]:
            self.show_landmarks = not self.show_landmarks
            status = "activados" if self.show_landmarks else "desactivados"
            print(f"🎯 Landmarks {status}")
        
        return True
    
    def run(self, camera_id=0):
        """
        Ejecuta la aplicación principal.
        
        Args:
            camera_id: ID de la cámara a utilizar
        """
        # Inicializar cámara
        if not self.initialize_camera(camera_id):
            return
        
        self.running = True
        print("\n🚀 Aplicación iniciada. Presiona ESC o Q para salir.")
        
        # Crear ventana explícitamente antes del bucle
        window_name = 'Hand Gesture Recognition'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 800, 600)
        cv2.moveWindow(window_name, 100, 100)
        
        try:
            print("🎬 Iniciando bucle principal de video...")
            print("📺 La ventana debería aparecer ahora...")
            frame_count = 0
            
            while self.running:
                # Leer frame
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Error al leer el frame de la cámara")
                    break
                
                frame_count += 1
                if frame_count == 1:
                    print("✅ Primer frame procesado - ¡La ventana debería estar visible!")
                elif frame_count % 120 == 0:  # Log cada 4 segundos aprox
                    print(f"📺 Frames procesados: {frame_count}")
                
                # Procesar frame
                processed_frame, hands_info = self.process_frame(frame)
                
                # Actualizar FPS
                fps = self.fps_counter.update()
                
                # Dibujar interfaz
                self.draw_interface(processed_frame, hands_info, fps)
                
                # Mostrar frame
                cv2.imshow(window_name, processed_frame)
                
                # Manejar entrada de teclado
                key = cv2.waitKey(1) & 0xFF
                if key != 255:  # Si se presionó alguna tecla
                    if not self.handle_keyboard_input(key, processed_frame, hands_info):
                        break
        
        except KeyboardInterrupt:
            print("\n⚡ Interrupción por teclado detectada")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """
        Limpia recursos y cierra la aplicación.
        """
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("🧹 Recursos liberados. ¡Hasta luego!")


def main():
    """
    Función principal de la aplicación.
    """
    print("🖐️ Iniciando Hand Gesture Recognition App...")
    print("=" * 50)
    
    app = HandGestureApp()
    app.run(camera_id=0)


if __name__ == "__main__":
    main()