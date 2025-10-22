# 🏖️ Selfie vs Selfie

**Juego multijugador de Piedra, Papel o Tijera con reconocimiento de gestos**  
_Estética inspirada en Playa del Carmen_ 🌊

![Demo](https://img.shields.io/badge/Status-Ready_for_Deployment-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎮 Características

- **🤝 Multijugador en tiempo real** - Crea salas y juega contra otros jugadores online
- **🤖 Modo IA** - Juega contra la inteligencia artificial cuando no hay jugadores disponibles
- **📸 Reconocimiento de gestos** - Usa tu cámara web para detectar piedra, papel o tijera
- **�️ Estética Playa del Carmen** - Diseño tropical con colores turquesa y arena
- **⚡ Tiempo real** - Comunicación instantánea con WebSockets
- **📱 Responsive** - Funciona en desktop y móvil
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
