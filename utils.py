import cv2
import numpy as np
import time
import math


def calculate_angle(point1, point2, point3):
    """
    Calcula el ángulo entre tres puntos.
    
    Args:
        point1, point2, point3: Coordenadas [x, y] de los puntos
        
    Returns:
        angle: Ángulo en grados
    """
    # Vectores desde point2 a point1 y point3
    vector1 = np.array([point1[0] - point2[0], point1[1] - point2[1]])
    vector2 = np.array([point3[0] - point2[0], point3[1] - point2[1]])
    
    # Calcular el ángulo usando el producto punto
    cos_angle = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    cos_angle = np.clip(cos_angle, -1.0, 1.0)  # Evitar errores de precisión
    angle = np.arccos(cos_angle)
    
    return np.degrees(angle)


def calculate_distance(point1, point2):
    """
    Calcula la distancia euclidiana entre dos puntos.
    
    Args:
        point1, point2: Coordenadas [x, y] de los puntos
        
    Returns:
        distance: Distancia euclidiana
    """
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


class FPSCounter:
    """
    Clase para medir y mostrar FPS (Frames Per Second).
    """
    def __init__(self):
        self.prev_time = time.time()
        self.fps_history = []
        self.max_history = 30  # Mantener los últimos 30 valores para promedio
        
    def update(self):
        """
        Actualiza el cálculo de FPS.
        
        Returns:
            fps: FPS actual
        """
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        
        # Mantener historial para promedio suavizado
        self.fps_history.append(fps)
        if len(self.fps_history) > self.max_history:
            self.fps_history.pop(0)
            
        return sum(self.fps_history) / len(self.fps_history)
    
    def draw_fps(self, image, fps):
        """
        Dibuja el FPS en la imagen.
        
        Args:
            image: Imagen donde dibujar
            fps: Valor de FPS a mostrar
        """
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(image, fps_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


def draw_gesture_info(image, gesture_info, position=(10, 70)):
    """
    Dibuja información del gesto en la imagen con mejor visibilidad.
    
    Args:
        image: Imagen donde dibujar
        gesture_info: Diccionario con información del gesto
        position: Posición inicial para el texto
    """
    x, y = position
    line_height = 40
    
    # Crear fondo semi-transparente para mejor legibilidad
    overlay = image.copy()
    cv2.rectangle(overlay, (x-5, y-30), (x+350, y+200), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, image, 0.4, 0, image)
    
    # Información básica con texto más grande y contorno
    draw_text_with_outline(image, f"DEDOS: {gesture_info['fingers_count']}", 
                          (x, y), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0), 3)
    
    draw_text_with_outline(image, f"GESTO: {gesture_info['gesture_name']}", 
                          (x, y + line_height), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
    
    # Piedra, papel, tijeras con colores distintivos
    rps_color = (0, 255, 0) if gesture_info['rps_gesture'] != "unknown" else (0, 0, 255)
    draw_text_with_outline(image, f"RPS: {gesture_info['rps_name']}", 
                          (x, y + 2*line_height), cv2.FONT_HERSHEY_DUPLEX, 0.8, rps_color, 2)
    
    # Gestos especiales
    if gesture_info['is_pointing']:
        draw_text_with_outline(image, f"SEÑALANDO: {gesture_info['point_direction'].upper()}", 
                              (x, y + 3*line_height), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 0, 255), 2)
    
    if gesture_info['thumbs_gesture']:
        thumb_text = "PULGAR ARRIBA" if gesture_info['thumbs_gesture'] == "thumbs_up" else "PULGAR ABAJO"
        draw_text_with_outline(image, thumb_text, 
                              (x, y + 4*line_height), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 2)
    
    if gesture_info['is_peace_sign']:
        draw_text_with_outline(image, "SIGNO DE PAZ", 
                              (x, y + 5*line_height), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 0), 2)

def draw_text_with_outline(image, text, position, font, scale, color, thickness):
    """
    Dibuja texto con contorno negro para mejor visibilidad.
    """
    x, y = position
    # Contorno negro
    cv2.putText(image, text, (x-2, y-2), font, scale, (0, 0, 0), thickness+2)
    cv2.putText(image, text, (x+2, y-2), font, scale, (0, 0, 0), thickness+2)
    cv2.putText(image, text, (x-2, y+2), font, scale, (0, 0, 0), thickness+2)
    cv2.putText(image, text, (x+2, y+2), font, scale, (0, 0, 0), thickness+2)
    # Texto principal
    cv2.putText(image, text, position, font, scale, color, thickness)


def draw_controls_info(image):
    """
    Dibuja información de controles en la imagen.
    
    Args:
        image: Imagen donde dibujar la información
    """
    h, w = image.shape[:2]
    controls = [
        "Controles:",
        "ESC/Q: Salir",
        "C: Cambiar modo",
        "R: Reiniciar",
        "S: Captura"
    ]
    
    # Fondo semi-transparente
    overlay = image.copy()
    cv2.rectangle(overlay, (w - 200, 10), (w - 10, 200), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.3, image, 0.7, 0, image)
    
    # Texto de controles
    for i, control in enumerate(controls):
        y_pos = 40 + i * 30
        color = (0, 255, 255) if i == 0 else (255, 255, 255)
        thickness = 2 if i == 0 else 1
        cv2.putText(image, control, (w - 190, y_pos), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)


def create_gesture_visualization(gesture_info, width=300, height=400):
    """
    Crea una visualización de los dedos levantados.
    
    Args:
        gesture_info: Diccionario con información del gesto
        width, height: Dimensiones de la imagen
        
    Returns:
        vis_image: Imagen con visualización de dedos
    """
    vis_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Nombres de dedos
    finger_names = ["Pulgar", "Índice", "Medio", "Anular", "Meñique"]
    finger_status = gesture_info['finger_status']
    
    # Dibujar estado de cada dedo
    for i, (name, is_up) in enumerate(zip(finger_names, finger_status)):
        y_pos = 50 + i * 60
        color = (0, 255, 0) if is_up else (0, 0, 255)
        
        # Círculo indicador
        cv2.circle(vis_image, (50, y_pos), 20, color, -1)
        
        # Nombre del dedo
        cv2.putText(vis_image, name, (90, y_pos + 7), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Estado
        status_text = "UP" if is_up else "DOWN"
        cv2.putText(vis_image, status_text, (200, y_pos + 7), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    # Contador total
    cv2.putText(vis_image, f"Total: {gesture_info['fingers_count']}", 
               (width//2 - 50, height - 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    
    return vis_image


def save_screenshot(image, gesture_info, counter=None):
    """
    Guarda una captura de pantalla con información del gesto.
    
    Args:
        image: Imagen a guardar
        gesture_info: Información del gesto
        counter: Contador para nombres únicos
        
    Returns:
        filename: Nombre del archivo guardado
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    if counter:
        filename = f"gesture_capture_{timestamp}_{counter}.jpg"
    else:
        filename = f"gesture_capture_{timestamp}.jpg"
    
    # Agregar información del gesto en la imagen
    info_text = f"Dedos: {gesture_info['fingers_count']} | {gesture_info['rps_name']}"
    cv2.putText(image, info_text, (10, image.shape[0] - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    cv2.imwrite(filename, image)
    return filename


def normalize_landmarks(landmarks, image_width, image_height):
    """
    Normaliza los landmarks a coordenadas relativas [0-1].
    
    Args:
        landmarks: Lista de coordenadas [x, y] absolutas
        image_width, image_height: Dimensiones de la imagen
        
    Returns:
        normalized_landmarks: Coordenadas normalizadas
    """
    normalized = []
    for x, y in landmarks:
        norm_x = x / image_width
        norm_y = y / image_height
        normalized.append([norm_x, norm_y])
    
    return normalized


def smooth_landmarks(current_landmarks, previous_landmarks, alpha=0.7):
    """
    Suaviza los landmarks usando un filtro de paso bajo.
    
    Args:
        current_landmarks: Landmarks actuales
        previous_landmarks: Landmarks del frame anterior
        alpha: Factor de suavizado (0-1)
        
    Returns:
        smoothed_landmarks: Landmarks suavizados
    """
    if previous_landmarks is None or len(previous_landmarks) != len(current_landmarks):
        return current_landmarks
    
    smoothed = []
    for curr, prev in zip(current_landmarks, previous_landmarks):
        smooth_x = alpha * curr[0] + (1 - alpha) * prev[0]
        smooth_y = alpha * curr[1] + (1 - alpha) * prev[1]
        smoothed.append([int(smooth_x), int(smooth_y)])
    
    return smoothed