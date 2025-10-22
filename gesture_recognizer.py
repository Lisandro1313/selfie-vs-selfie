import cv2
import numpy as np
from utils import calculate_angle


class GestureRecognizer:
    def __init__(self):
        """
        Inicializa el reconocedor de gestos.
        """
        self.gesture_names = {
            0: "Puño cerrado",
            1: "Uno",
            2: "Dos", 
            3: "Tres",
            4: "Cuatro",
            5: "Cinco (Mano abierta)"
        }
        
        self.rps_gestures = {
            "rock": "Piedra 🗿",
            "paper": "Papel 📄", 
            "scissors": "Tijeras ✂️",
            "unknown": "Desconocido ❓"
        }
        
    def count_fingers(self, landmarks):
        """
        Cuenta el número de dedos levantados basándose en los landmarks de la mano.
        
        Args:
            landmarks: Lista de coordenadas [x, y] de los landmarks de la mano
            
        Returns:
            fingers_up: Número de dedos levantados (0-5)
            finger_status: Lista booleana indicando el estado de cada dedo
        """
        if len(landmarks) != 21:
            return 0, [False] * 5
        
        finger_status = []
        
        # Pulgar - mejorado para detectar mejor la orientación
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        
        # Calcular si el pulgar está extendido basado en la distancia
        thumb_extended = self._is_thumb_extended(thumb_tip, thumb_ip, thumb_mcp)
        finger_status.append(thumb_extended)
        
        # Otros cuatro dedos - usar múltiples puntos para mejor detección
        finger_tips = [8, 12, 16, 20]  # Índice, medio, anular, meñique
        finger_pips = [6, 10, 14, 18]  # Articulaciones proximales
        finger_mcps = [5, 9, 13, 17]   # Articulaciones metacarpianas
        
        for tip, pip, mcp in zip(finger_tips, finger_pips, finger_mcps):
            # Un dedo está levantado si la punta está significativamente arriba del PIP
            # y también está arriba del MCP
            finger_extended = (landmarks[tip][1] < landmarks[pip][1] - 10 and 
                             landmarks[tip][1] < landmarks[mcp][1])
            finger_status.append(finger_extended)
        
        fingers_up = sum(finger_status)
        return fingers_up, finger_status
    
    def _is_thumb_extended(self, thumb_tip, thumb_ip, thumb_mcp):
        """
        Determina si el pulgar está extendido usando geometría mejorada.
        """
        # Calcular distancias
        tip_to_mcp = np.sqrt((thumb_tip[0] - thumb_mcp[0])**2 + (thumb_tip[1] - thumb_mcp[1])**2)
        ip_to_mcp = np.sqrt((thumb_ip[0] - thumb_mcp[0])**2 + (thumb_ip[1] - thumb_mcp[1])**2)
        
        # El pulgar está extendido si la punta está más lejos del MCP que el IP
        return tip_to_mcp > ip_to_mcp * 1.2
    
    def recognize_rock_paper_scissors(self, landmarks):
        """
        Reconoce gestos de piedra, papel o tijeras con mejor precisión.
        
        Args:
            landmarks: Lista de coordenadas [x, y] de los landmarks de la mano
            
        Returns:
            gesture: Gesto reconocido ("rock", "paper", "scissors", "unknown")
        """
        fingers_up, finger_status = self.count_fingers(landmarks)
        
        # Piedra: Puño cerrado (0 o 1 dedo máximo)
        if fingers_up <= 1:
            # Verificar que realmente sea un puño - todos los dedos doblados
            if self._is_closed_fist(landmarks):
                return "rock"
        
        # Papel: Mano abierta (4 o 5 dedos)
        elif fingers_up >= 4:
            # Verificar que los dedos estén bien separados
            if self._is_open_hand(landmarks, finger_status):
                return "paper"
        
        # Tijeras: Índice y medio levantados (más flexible)
        elif fingers_up == 2 or fingers_up == 3:
            # Verificar que al menos índice y medio estén levantados
            if finger_status[1] and finger_status[2]:
                # Verificar que pulgar, anular y meñique no estén muy extendidos
                if self._is_scissors_gesture(landmarks):
                    return "scissors"
        
        return "unknown"
    
    def _is_closed_fist(self, landmarks):
        """Verifica si realmente es un puño cerrado"""
        # Verificar que las puntas de los dedos estén cerca de las palmas
        finger_tips = [8, 12, 16, 20]  # Índice, medio, anular, meñique
        palm_center = landmarks[9]  # Centro aproximado de la palma
        
        close_fingers = 0
        for tip in finger_tips:
            distance = np.sqrt((landmarks[tip][0] - palm_center[0])**2 + 
                             (landmarks[tip][1] - palm_center[1])**2)
            if distance < 60:  # Ajustar según el tamaño de mano
                close_fingers += 1
        
        return close_fingers >= 3
    
    def _is_open_hand(self, landmarks, finger_status):
        """Verifica si es una mano abierta real"""
        # Al menos 4 dedos deben estar levantados
        extended_fingers = sum(finger_status)
        return extended_fingers >= 4
    
    def _is_scissors_gesture(self, landmarks):
        """Verifica si es realmente el gesto de tijeras con criterios mejorados"""
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        thumb_tip = landmarks[4]
        
        # Verificar que índice y medio estén extendidos y separados
        distance_index_middle = np.sqrt((index_tip[0] - middle_tip[0])**2 + 
                                       (index_tip[1] - middle_tip[1])**2)
        
        # Verificar que anular y meñique estén más bajos (doblados)
        palm_y = landmarks[9][1]  # Punto de referencia en la palma
        
        # Índice y medio deben estar arriba del nivel de la palma (más flexible)
        index_extended = index_tip[1] < palm_y - 10
        middle_extended = middle_tip[1] < palm_y - 10
        
        # Anular y meñique deben estar cerca del nivel de la palma o abajo (más flexible)
        ring_folded = ring_tip[1] > palm_y - 40
        pinky_folded = pinky_tip[1] > palm_y - 40
        
        # Los dedos índice y medio deben estar separados (formando V) - umbral más bajo
        fingers_separated = distance_index_middle > 20
        
        return (index_extended and middle_extended and 
                ring_folded and pinky_folded and fingers_separated)
    
    def detect_pointing_gesture(self, landmarks):
        """
        Detecta si la mano está señalando.
        
        Args:
            landmarks: Lista de coordenadas [x, y] de los landmarks de la mano
            
        Returns:
            is_pointing: True si está señalando, False en caso contrario
            direction: Dirección general del dedo índice
        """
        fingers_up, finger_status = self.count_fingers(landmarks)
        
        # Solo el dedo índice levantado
        if fingers_up == 1 and finger_status[1]:
            # Calcular dirección del dedo índice
            index_tip = landmarks[8]
            index_mcp = landmarks[5]  # Base del dedo índice
            
            dx = index_tip[0] - index_mcp[0]
            dy = index_tip[1] - index_mcp[1]
            
            # Determinar dirección
            if abs(dx) > abs(dy):
                direction = "derecha" if dx > 0 else "izquierda"
            else:
                direction = "arriba" if dy < 0 else "abajo"
            
            return True, direction
        
        return False, None
    
    def detect_thumbs_up_down(self, landmarks):
        """
        Detecta gestos de pulgar arriba o abajo.
        
        Args:
            landmarks: Lista de coordenadas [x, y] de los landmarks de la mano
            
        Returns:
            gesture: "thumbs_up", "thumbs_down", o None
        """
        fingers_up, finger_status = self.count_fingers(landmarks)
        
        # Solo el pulgar levantado
        if fingers_up == 1 and finger_status[0]:
            thumb_tip = landmarks[4]
            thumb_mcp = landmarks[2]  # Base del pulgar
            
            # Si la punta del pulgar está significativamente arriba de su base
            if thumb_tip[1] < thumb_mcp[1] - 30:
                return "thumbs_up"
            # Si la punta del pulgar está significativamente abajo de su base  
            elif thumb_tip[1] > thumb_mcp[1] + 30:
                return "thumbs_down"
        
        return None
    
    def detect_peace_sign(self, landmarks):
        """
        Detecta el signo de la paz (V con índice y medio).
        
        Args:
            landmarks: Lista de coordenadas [x, y] de los landmarks de la mano
            
        Returns:
            is_peace: True si es signo de paz, False en caso contrario
        """
        fingers_up, finger_status = self.count_fingers(landmarks)
        
        # Índice y medio levantados (más flexible para paz vs tijeras)
        if fingers_up >= 2 and finger_status[1] and finger_status[2]:
            
            # Verificar que índice y medio estén separados (signo V)
            index_tip = landmarks[8]
            middle_tip = landmarks[12]
            distance = np.sqrt((index_tip[0] - middle_tip[0])**2 + 
                             (index_tip[1] - middle_tip[1])**2)
            
            # Para paz, los dedos suelen estar más separados que para tijeras
            if distance > 35:
                return True
        
        return False
    
    def get_gesture_info(self, landmarks):
        """
        Obtiene información completa del gesto detectado.
        
        Args:
            landmarks: Lista de coordenadas [x, y] de los landmarks de la mano
            
        Returns:
            gesture_info: Diccionario con información del gesto
        """
        fingers_up, finger_status = self.count_fingers(landmarks)
        rps_gesture = self.recognize_rock_paper_scissors(landmarks)
        is_pointing, point_direction = self.detect_pointing_gesture(landmarks)
        thumbs_gesture = self.detect_thumbs_up_down(landmarks)
        is_peace = self.detect_peace_sign(landmarks)
        
        gesture_info = {
            'fingers_count': fingers_up,
            'finger_status': finger_status,
            'gesture_name': self.gesture_names.get(fingers_up, "Desconocido"),
            'rps_gesture': rps_gesture,
            'rps_name': self.rps_gestures.get(rps_gesture, "Desconocido"),
            'is_pointing': is_pointing,
            'point_direction': point_direction,
            'thumbs_gesture': thumbs_gesture,
            'is_peace_sign': is_peace
        }
        
        return gesture_info