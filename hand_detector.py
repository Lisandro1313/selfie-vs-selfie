import cv2
import mediapipe as mp
import numpy as np


class HandDetector:
    def __init__(self, static_image_mode=False, max_num_hands=2, 
                 min_detection_confidence=0.7, min_tracking_confidence=0.5):
        """
        Inicializa el detector de manos usando MediaPipe.
        
        Args:
            static_image_mode: Si True, trata cada imagen como independiente
            max_num_hands: Número máximo de manos a detectar
            min_detection_confidence: Confianza mínima para detección
            min_tracking_confidence: Confianza mínima para tracking
        """
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        # Inicializar MediaPipe con configuración optimizada
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=0.8,  # Aumentar confianza para mejor detección
            min_tracking_confidence=0.7,   # Aumentar tracking para más estabilidad
            model_complexity=1             # Usar modelo más complejo para mejor precisión
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Conexiones de los puntos clave
        self.hand_connections = self.mp_hands.HAND_CONNECTIONS
        
    def detect_hands(self, image, draw=True):
        """
        Detecta manos en una imagen y opcionalmente dibuja los landmarks.
        
        Args:
            image: Imagen de entrada (BGR)
            draw: Si True, dibuja los landmarks en la imagen
            
        Returns:
            image: Imagen con landmarks dibujados (si draw=True)
            hands_data: Lista con información de las manos detectadas
        """
        # Convertir BGR a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        
        # Procesar la imagen
        results = self.hands.process(image_rgb)
        
        # Convertir de vuelta a BGR
        image_rgb.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        hands_data = []
        
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Obtener información de la mano (izquierda o derecha)
                hand_label = results.multi_handedness[idx].classification[0].label
                hand_score = results.multi_handedness[idx].classification[0].score
                
                # Extraer coordenadas de los landmarks
                landmarks = []
                h, w, c = image.shape
                
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append([cx, cy])
                
                hands_data.append({
                    'landmarks': landmarks,
                    'label': hand_label,
                    'score': hand_score,
                    'raw_landmarks': hand_landmarks
                })
                
                # Dibujar landmarks si se solicita
                if draw:
                    self.mp_drawing.draw_landmarks(
                        image, hand_landmarks, self.hand_connections,
                        self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                    )
                    
                    # Dibujar etiqueta de la mano
                    cv2.putText(image, f"{hand_label} ({hand_score:.2f})", 
                              (landmarks[0][0], landmarks[0][1] - 20),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return image, hands_data
    
    def get_finger_positions(self, landmarks):
        """
        Obtiene las posiciones de las puntas de los dedos.
        
        Args:
            landmarks: Lista de coordenadas [x, y] de los landmarks
            
        Returns:
            finger_tips: Diccionario con las posiciones de las puntas de los dedos
        """
        if len(landmarks) < 21:
            return None
            
        finger_tips = {
            'thumb': landmarks[4],      # Pulgar
            'index': landmarks[8],      # Índice
            'middle': landmarks[12],    # Medio
            'ring': landmarks[16],      # Anular
            'pinky': landmarks[20]      # Meñique
        }
        
        return finger_tips
    
    def calculate_distance(self, point1, point2):
        """
        Calcula la distancia euclidiana entre dos puntos.
        
        Args:
            point1: Coordenadas [x, y] del primer punto
            point2: Coordenadas [x, y] del segundo punto
            
        Returns:
            distance: Distancia euclidiana
        """
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def get_hand_center(self, landmarks):
        """
        Calcula el centro de la mano basado en los landmarks.
        
        Args:
            landmarks: Lista de coordenadas [x, y] de los landmarks
            
        Returns:
            center: Coordenadas [x, y] del centro de la mano
        """
        if not landmarks:
            return None
            
        x_coords = [lm[0] for lm in landmarks]
        y_coords = [lm[1] for lm in landmarks]
        
        center_x = sum(x_coords) // len(x_coords)
        center_y = sum(y_coords) // len(y_coords)
        
        return [center_x, center_y]