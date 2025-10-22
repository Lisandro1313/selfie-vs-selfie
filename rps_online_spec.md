# 🎮 Rock Paper Scissors Online - Multijugador con Reconocimiento de Gestos

## Descripción del Proyecto

Juego online multijugador de piedra-papel-tijeras que utiliza reconocimiento de gestos con cámara web. Los jugadores se conectan a salas, hacen sus gestos simultáneamente, y el sistema determina automáticamente el ganador.

## 🚀 Funcionalidades

### 🏠 Lobby Principal

- Ingreso de alias/nombre de usuario
- Creación o unión a salas (Room 1, Room 2, etc.)
- Lista de salas disponibles y jugadores conectados

### 🎯 Sistema de Salas

- Máximo 2 jugadores por sala
- Cuando se completan 2 jugadores, inicia automáticamente
- Chat básico entre jugadores en espera

### 🖐️ Gameplay

- Countdown simultáneo (3, 2, 1, ¡YA!)
- Detección de gestos en tiempo real
- Cada jugador solo ve su propia cámara durante el juego
- Captura automática del gesto al final del countdown

### 🏆 Resultados

- Pantalla con ambas capturas lado a lado
- Detección automática del gesto de cada jugador
- Declaración del ganador con lógica RPS
- Opción de jugar otra ronda o cambiar de sala

## 🛠️ Stack Tecnológico

### Backend

- **Flask**: Servidor web principal
- **Flask-SocketIO**: Comunicación en tiempo real
- **OpenCV + MediaPipe**: Procesamiento de gestos
- **PIL**: Manipulación de imágenes
- **Base64**: Transferencia de imágenes

### Frontend

- **HTML5 + CSS3**: Interfaz responsive
- **JavaScript**: Lógica del cliente
- **Socket.IO**: Comunicación bidireccional
- **WebRTC**: Acceso a cámara web
- **Bootstrap**: Styling moderno

## 📁 Estructura del Proyecto

```
rps_online/
├── app.py                 # Servidor Flask principal
├── game_logic.py          # Lógica del juego RPS
├── gesture_detector.py    # Detección de gestos (adaptado)
├── templates/
│   ├── index.html        # Página principal/lobby
│   ├── game.html         # Sala de juego
│   └── results.html      # Pantalla de resultados
├── static/
│   ├── css/
│   │   └── style.css     # Estilos principales
│   ├── js/
│   │   ├── lobby.js      # Lógica del lobby
│   │   ├── game.js       # Lógica del juego
│   │   └── camera.js     # Manejo de cámara
│   └── images/           # Assets del juego
└── requirements.txt      # Dependencias del proyecto
```

## 🎮 Flujo del Juego

1. **Ingreso**: Usuario entra, pone alias
2. **Lobby**: Ve salas disponibles, elige una
3. **Espera**: Aguarda a que se complete la sala (2/2)
4. **Preparación**: Ambos ven countdown y sus cámaras
5. **Acción**: 3-2-1 countdown, hacen gesto simultáneo
6. **Captura**: Screenshot automático de ambos
7. **Análisis**: IA determina gesto de cada uno
8. **Resultado**: Muestra capturas + ganador
9. **Repetir**: Opción de nueva ronda o cambiar sala

## 🔧 Características Técnicas

### Comunicación Real-Time

- WebSockets para sincronización
- Estados de juego compartidos
- Heartbeat para conexiones

### Procesamiento de Imágenes

- Detección de gestos optimizada
- Capturas en alta calidad
- Compresión para transferencia rápida

### Seguridad y Performance

- Validación de gestos server-side
- Rate limiting para evitar spam
- Cleanup automático de salas vacías

¿Te gusta esta estructura? ¿Quieres que empiece a desarrollarlo?
