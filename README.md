# Hand Detection & Gesture Recognition

Un proyecto de detección de manos y reconocimiento de gestos en tiempo real usando OpenCV y MediaPipe.

## Características

- 🖐️ Detección de manos en tiempo real
- 📊 Visualización de puntos clave de la mano
- ✋ Reconocimiento de gestos (contar dedos, piedra-papel-tijeras)
- 🎮 Controles interactivos
- 📈 Monitoreo de FPS y rendimiento

## Requisitos

- Python 3.8+
- Cámara web
- Windows/macOS/Linux

## Instalación

1. Clona este repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta la aplicación principal:

```bash
python main.py
```

### Controles

- **ESC** o **Q**: Salir de la aplicación
- **C**: Cambiar modo de reconocimiento
- **R**: Reiniciar contador
- **S**: Guardar captura de pantalla

## Gestos Reconocidos

- **Contar dedos**: Muestra cuántos dedos tienes levantados (0-5)
- **Piedra**: Puño cerrado
- **Papel**: Mano abierta
- **Tijeras**: Dos dedos extendidos

## Estructura del Proyecto

```
renoconocimientoFa/
├── main.py              # Aplicación principal
├── hand_detector.py     # Lógica de detección de manos
├── gesture_recognizer.py # Clasificación de gestos
├── utils.py            # Funciones utilitarias
├── requirements.txt    # Dependencias de Python
└── README.md          # Este archivo
```

## Tecnologías

- **OpenCV**: Procesamiento de imágenes y video
- **MediaPipe**: Framework de ML para detección de manos
- **NumPy**: Operaciones matemáticas y arrays

## Contribución

¡Las contribuciones son bienvenidas! Siéntete libre de abrir issues o enviar pull requests.

## Licencia

Este proyecto está bajo la Licencia MIT.
