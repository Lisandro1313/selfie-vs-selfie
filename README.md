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
- **🏖️ Estética Playa del Carmen** - Diseño tropical con colores turquesa y arena
- **⚡ Tiempo real** - Comunicación instantánea con WebSockets
- **📱 Responsive** - Funciona en desktop y móvil
- **📈 Monitoreo** - Sistema de puntuación y estadísticas

## 🚀 Inicio Rápido

### 🌐 Juego Online (Recomendado)

```bash
# Instalación automática (Windows)
install.bat

# Ejecutar servidor
run_game.bat

# O manualmente:
python rps_online/run_server.py
```

**Luego abre**: `http://localhost:5000`

### 🖥️ Versión Local

```bash
python main.py
```

## 📋 Requisitos

- Python 3.8+
- Cámara web
- Windows/macOS/Linux
- Navegador moderno (para versión online)

## 📦 Instalación Completa

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/Lisandro1313/selfie-vs-selfie.git
   cd selfie-vs-selfie
   ```

2. **Instala dependencias**

   ```bash
   pip install -r requirements.txt
   pip install -r rps_online/requirements.txt
   ```

3. **Ejecuta el juego**
   - **Online**: `python rps_online/run_server.py`
   - **Local**: `python main.py`

## 🎯 Modos de Juego

### 🌐 Multijugador Online

- **Crear Sala**: Genera una sala privada y comparte el código
- **Unirse a Sala**: Busca salas disponibles y únete instantáneamente
- **Modo IA**: Juega contra inteligencia artificial sin esperas
- **Tiempo Real**: Comunicación instantánea con WebSockets

### 🖥️ Local (Solo)

- **Práctica**: Perfecciona tus gestos
- **Contador de dedos**: Detecta cuántos dedos tienes levantados
- **Calibración**: Ajusta el reconocimiento según tu cámara

## 🎮 Controles

### Versión Online

- **Navegador**: Interfaz web intuitiva
- **Cámara**: Reconocimiento automático de gestos
- **Responsive**: Funciona en móvil y desktop

### Versión Local

- **ESC** o **Q**: Salir de la aplicación
- **C**: Cambiar modo de reconocimiento
- **R**: Reiniciar contador
- **S**: Guardar captura de pantalla

## Gestos Reconocidos

- **Contar dedos**: Muestra cuántos dedos tienes levantados (0-5)
- **Piedra**: Puño cerrado
- **Papel**: Mano abierta
- **Tijeras**: Dos dedos extendidos

## 📁 Estructura del Proyecto

```
selfie-vs-selfie/
├── 🌐 rps_online/          # Versión multijugador online
│   ├── app.py              # Servidor Flask principal
│   ├── run_server.py       # Script de ejecución mejorado
│   ├── gesture_detector.py # Detección de gestos online
│   ├── requirements.txt    # Dependencias web
│   ├── templates/          # Páginas HTML
│   │   ├── index.html      # Lobby principal
│   │   └── game.html       # Sala de juego
│   └── static/             # CSS, JS, assets
│       ├── css/style.css   # Estilos Playa del Carmen
│       └── js/             # Lógica frontend
├── 🖥️ Versión Local
│   ├── main.py             # Aplicación principal local
│   ├── hand_detector.py    # Detector de manos
│   ├── gesture_recognizer.py # Clasificador de gestos
│   └── utils.py            # Funciones utilitarias
├── 📦 Configuración
│   ├── requirements.txt    # Dependencias principales
│   ├── install.bat         # Instalador automático
│   └── run_game.bat        # Ejecutor del servidor
└── 📚 Documentación
    ├── README.md           # Esta guía
    ├── JUEGO_ONLINE_GUIA.md # Guía detallada online
    └── DEPLOYMENT_GUIDE.md # Guía de despliegue
```

## 🛠️ Tecnologías

### Backend

- **Flask**: Framework web ligero
- **SocketIO**: Comunicación en tiempo real
- **OpenCV**: Procesamiento de video
- **MediaPipe**: ML para detección de manos

### Frontend

- **HTML5**: Estructura moderna
- **CSS3**: Estilos responsive con tema tropical
- **JavaScript**: Lógica del juego y WebSockets
- **WebRTC**: Acceso a cámara web

### Machine Learning

- **MediaPipe Hands**: Detección precisa de manos
- **Custom Classifier**: Algoritmo de clasificación de gestos
- **Real-time Processing**: Procesamiento en tiempo real

## 🤝 Contribución

¡Las contribuciones son bienvenidas!

### Cómo Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

### Ideas para Contribuir

- 🎨 Nuevos temas visuales
- 🎮 Modos de juego adicionales
- 🌍 Internacionalización
- 📱 Mejoras móviles
- 🤖 IA más inteligente

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Lisandro Etcheverry**

- GitHub: [@Lisandro1313](https://github.com/Lisandro1313)
- Proyecto: [selfie-vs-selfie](https://github.com/Lisandro1313/selfie-vs-selfie)

## 🙏 Agradecimientos

- **MediaPipe** por el framework de ML
- **Flask-SocketIO** por la comunicación en tiempo real
- **OpenCV** por el procesamiento de video
- **Playa del Carmen** por la inspiración visual 🏖️

---

**¡Disfruta jugando Selfie vs Selfie!** 🎉🎯🏆
