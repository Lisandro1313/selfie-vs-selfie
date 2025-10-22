import cv2
import mediapipe as mp
import numpy as np

class GestureDetector:
    def __init__(self):
        """
        Detector de gestos optimizado para el juego online.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7,
            model_complexity=1
        )
        
        self.rps_gestures = {
            "rock": "piedra",
            "paper": "papel", 
            "scissors": "tijeras",
            "unknown": "desconocido"
        }
    
    def detect_rps_gesture(self, image):
        """
        Detecta gesto de piedra, papel o tijeras en una imagen.
        
        Args:
            image: Imagen BGR de OpenCV
            
        Returns:
            gesture: "rock", "paper", "scissors", o "unknown"
        """
        # Convertir BGR a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            # Tomar la primera mano detectada
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Convertir landmarks a coordenadas
            h, w = image.shape[:2]
            landmarks = []
            for lm in hand_landmarks.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append([cx, cy])
            
            # Reconocer gesto
            return self._classify_rps_gesture(landmarks)
        
        return "unknown"
    
    def _classify_rps_gesture(self, landmarks):
        """
        Clasifica el gesto basado en los landmarks.
        """
        if len(landmarks) != 21:
            return "unknown"
        
        fingers_up = self._count_fingers(landmarks)
        
        # Piedra: Puño cerrado (0-1 dedos)
        if fingers_up <= 1:
            if self._is_closed_fist(landmarks):
                return "rock"
        
        # Papel: Mano abierta (4-5 dedos)
        elif fingers_up >= 4:
            if self._is_open_hand(landmarks):
                return "paper"
        
        # Tijeras: Índice y medio extendidos (2-3 dedos)
        elif fingers_up == 2 or fingers_up == 3:
            if self._is_scissors_gesture(landmarks):
                return "scissors"
        
        return "unknown"
    
    def _count_fingers(self, landmarks):
        """
        Cuenta dedos extendidos.
        """
        finger_status = []
        
        # Pulgar
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        thumb_extended = self._is_thumb_extended(thumb_tip, thumb_ip, thumb_mcp)
        finger_status.append(thumb_extended)
        
        # Otros dedos
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        finger_mcps = [5, 9, 13, 17]
        
        for tip, pip, mcp in zip(finger_tips, finger_pips, finger_mcps):
            finger_extended = (landmarks[tip][1] < landmarks[pip][1] - 10 and 
                             landmarks[tip][1] < landmarks[mcp][1])
            finger_status.append(finger_extended)
        
        return sum(finger_status)
    
    def _is_thumb_extended(self, thumb_tip, thumb_ip, thumb_mcp):
        """
        Verifica si el pulgar está extendido.
        """
        tip_to_mcp = np.sqrt((thumb_tip[0] - thumb_mcp[0])**2 + (thumb_tip[1] - thumb_mcp[1])**2)
        ip_to_mcp = np.sqrt((thumb_ip[0] - thumb_mcp[0])**2 + (thumb_ip[1] - thumb_mcp[1])**2)
        return tip_to_mcp > ip_to_mcp * 1.2
    
    def _is_closed_fist(self, landmarks):
        """
        Verifica si es un puño cerrado.
        """
        finger_tips = [8, 12, 16, 20]
        palm_center = landmarks[9]
        
        close_fingers = 0
        for tip in finger_tips:
            distance = np.sqrt((landmarks[tip][0] - palm_center[0])**2 + 
                             (landmarks[tip][1] - palm_center[1])**2)
            if distance < 80:
                close_fingers += 1
        
        return close_fingers >= 3
    
    def _is_open_hand(self, landmarks):
        """
        Verifica si es una mano abierta.
        """
        finger_tips = [4, 8, 12, 16, 20]
        palm_center = landmarks[9]
        
        extended_fingers = 0
        for tip in finger_tips:
            distance = np.sqrt((landmarks[tip][0] - palm_center[0])**2 + 
                             (landmarks[tip][1] - palm_center[1])**2)
            if distance > 60:
                extended_fingers += 1
        
        return extended_fingers >= 4
    
    def _is_scissors_gesture(self, landmarks):
        """
        Verifica si es el gesto de tijeras.
        """
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        palm_y = landmarks[9][1]
        
        # Verificar que índice y medio estén extendidos
        index_extended = index_tip[1] < palm_y - 15
        middle_extended = middle_tip[1] < palm_y - 15
        
        # Verificar que anular y meñique estén doblados
        ring_folded = ring_tip[1] > palm_y - 40
        pinky_folded = pinky_tip[1] > palm_y - 40
        
        # Verificar separación entre índice y medio
        distance = np.sqrt((index_tip[0] - middle_tip[0])**2 + 
                          (index_tip[1] - middle_tip[1])**2)
        fingers_separated = distance > 20
        
        return (index_extended and middle_extended and 
                ring_folded and pinky_folded and fingers_separated)