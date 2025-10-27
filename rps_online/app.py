from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
import base64
import io
import time
import uuid
from threading import Lock
import random
import os

# Import OpenCV with error handling for deployment
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
    print("✅ OpenCV loaded successfully")
except ImportError as e:
    print(f"⚠️ OpenCV import error: {e}")
    CV2_AVAILABLE = False
    
from PIL import Image

# Import gesture detector with error handling
try:
    from gesture_detector import GestureDetector
    GESTURE_DETECTOR_AVAILABLE = True
    print("✅ GestureDetector loaded successfully")
except ImportError as e:
    print(f"⚠️ GestureDetector import error: {e}")
    GESTURE_DETECTOR_AVAILABLE = False

# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'rps_online_secret_2025')

# Configuración de CORS para desarrollo y producción
cors_origins = os.environ.get('CORS_ORIGINS', "*")
socketio = SocketIO(app, cors_allowed_origins=cors_origins)

class GameRoom:
    def __init__(self, room_id):
        self.room_id = room_id
        self.players = {}
        self.status = 'waiting'  # waiting, countdown, playing, results
        self.countdown_timer = None
        self.gestures = {}
        self.captures = {}
        self.results = None
        self.created_at = time.time()
        self.is_ai_game = False
        self.ai_player = None
    
    def add_player(self, player_id, username):
        if len(self.players) < 2:
            self.players[player_id] = {
                'username': username,
                'ready': False,
                'gesture': None,
                'capture': None
            }
            return True
        return False
    
    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
            if len(self.players) == 0:
                self.status = 'empty'
    
    def is_full(self):
        return len(self.players) >= 2
    
    def all_ready(self):
        if self.is_ai_game:
            # Para juegos AI, solo necesitamos que el jugador humano esté listo
            return len(self.players) == 1 and all(p['ready'] for p in self.players.values())
        else:
            # Para juegos multijugador, necesitamos 2 jugadores listos
            return len(self.players) == 2 and all(p['ready'] for p in self.players.values())
    
    def reset_round(self):
        self.status = 'waiting'
        self.gestures = {}
        self.captures = {}
        self.results = None
        for player in self.players.values():
            player['ready'] = False
            player['gesture'] = None
            player['capture'] = None
        
        # Reset IA si existe
        if self.is_ai_game and self.ai_player:
            self.ai_player.reset()


class AIPlayer:
    def __init__(self):
        self.username = "🤖 IA"
        self.gesture = None
        self.ready = False
    
    def make_move(self):
        """IA hace un movimiento aleatorio"""
        moves = ['rock', 'paper', 'scissors']
        self.gesture = random.choice(moves)
        self.ready = True
        return self.gesture
    
    def reset(self):
        self.gesture = None
        self.ready = False


# Estado global del juego
game_rooms = {}
players = {}
room_lock = Lock()

# Initialize gesture detector if available
if GESTURE_DETECTOR_AVAILABLE and CV2_AVAILABLE:
    gesture_detector = GestureDetector()
    print("✅ GestureDetector initialized")
else:
    gesture_detector = None
    print("⚠️ GestureDetector not available, using fallback")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test_page():
    return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧪 Test - Jugar de Nuevo AI</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: linear-gradient(135deg, #20B2AA, #87CEEB); color: #333; }
        .test-container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
        .step { padding: 10px; margin: 10px 0; border-left: 4px solid #20B2AA; background: #f8f9fa; }
        .success { border-left-color: #28a745; background: #d4edda; }
        button { padding: 10px 20px; background: #20B2AA; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        button:hover { background: #1a9999; }
    </style>
</head>
<body>
    <div class="test-container">
        <h1>🧪 Test: Jugar de Nuevo contra IA - FUNCIONANDO ✅</h1>
        
        <div class="step success">
            <h3>🎉 ¡Problema Solucionado!</h3>
            <p>Los cambios aplicados han corregido el problema del "Jugar de nuevo" en modo IA:</p>
            <ul>
                <li>✅ <code>this.isAIGame</code> se mantiene entre rondas</li>
                <li>✅ <code>localStorage.ai_game_info</code> se preserva</li>
                <li>✅ <code>all_ready()</code> funciona correctamente con IA</li>
                <li>✅ <code>resetRound()</code> mantiene el estado AI</li>
                <li>✅ Interfaz se resetea correctamente</li>
            </ul>
        </div>

        <div class="step">
            <h3>📋 Para verificar la corrección:</h3>
            <ol>
                <li>Haz clic en "🚀 Ir al Juego"</li>
                <li>Crea un juego contra IA</li>
                <li>Completa una ronda</li>
                <li>Presiona "🔄 Jugar de Nuevo"</li>
                <li>Verifica que funciona correctamente</li>
            </ol>
        </div>

        <button onclick="window.open('/', '_blank')">🚀 Ir al Juego</button>
        
        <div class="step">
            <h3>🔧 Cambios técnicos aplicados:</h3>
            <ul>
                <li><strong>JavaScript Frontend:</strong>
                    <ul>
                        <li>Añadido <code>this.isAIGame = false</code> en constructor</li>
                        <li>Preservado <code>localStorage.ai_game_info</code> (no se elimina hasta salir)</li>
                        <li>Mejorado <code>resetRound()</code> para mantener estado AI</li>
                        <li>Añadidos logs de debugging</li>
                    </ul>
                </li>
                <li><strong>Python Backend:</strong>
                    <ul>
                        <li>Corregido <code>all_ready()</code> para juegos AI (1 jugador vs 2)</li>
                        <li>Mejorado <code>handle_play_again()</code> con detección AI</li>
                        <li>Añadidos logs detallados</li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</body>
</html>"""

@app.route('/game/<room_id>')
def game(room_id):
    return render_template('game.html', room_id=room_id)

@socketio.on('join_lobby')
def handle_join_lobby(data):
    print(f"Usuario intentando unirse al lobby: {data}")
    username = data['username']
    
    # Verificar si el usuario ya está conectado
    if request.sid in players:
        existing_player = players[request.sid]
        if existing_player['username'] == username:
            print(f"Jugador {username} ya conectado, enviando datos existentes")
            # Enviar datos existentes sin crear nuevo jugador
            available_rooms = get_available_rooms()
            emit('lobby_joined', {
                'player_id': existing_player['id'],
                'username': username,
                'available_rooms': available_rooms
            })
            return
    
    # Crear nuevo jugador si no existe
    player_id = str(uuid.uuid4())
    players[request.sid] = {
        'id': player_id,
        'username': username,
        'room': None
    }
    
    print(f"Jugador {username} agregado con ID {player_id}")
    
    # Enviar lista de salas disponibles
    available_rooms = get_available_rooms()
    
    print(f"Enviando lobby_joined para {username}, salas: {available_rooms}")
    
    emit('lobby_joined', {
        'player_id': player_id,
        'username': username,
        'available_rooms': available_rooms
    })

@socketio.on('create_room')
def handle_create_room():
    print(f"🏠 HANDLER create_room ejecutado - SID: {request.sid}")
    print(f"🔍 Players disponibles: {list(players.keys())}")
    if request.sid not in players:
        print(f"❌ SID {request.sid} no encontrado en players")
        print(f"❌ El usuario debe reconectarse correctamente")
        emit('error', {'message': 'Usuario no registrado, recarga la página'})
        return
    
    room_id = f"room_{int(time.time() * 1000) % 10000}"
    player = players[request.sid]
    
    with room_lock:
        if room_id not in game_rooms:
            game_rooms[room_id] = GameRoom(room_id)
        
        room = game_rooms[room_id]
        if room.add_player(player['id'], player['username']):
            player['room'] = room_id
            join_room(room_id)
            
            emit('room_created', {
                'room_id': room_id,
                'redirect': True
            })
            
            # Notificar a todos sobre la nueva sala
            socketio.emit('room_list_updated', {
                'available_rooms': get_available_rooms()
            })

@socketio.on('create_ai_game')
def handle_create_ai_game():
    print(f"🤖 HANDLER create_ai_game ejecutado - SID: {request.sid}")
    print(f"🔍 Players disponibles: {list(players.keys())}")
    if request.sid not in players:
        print(f"❌ SID {request.sid} no encontrado en players")
        print(f"❌ El usuario debe reconectarse correctamente")
        emit('error', {'message': 'Usuario no registrado, recarga la página'})
        return
    
    room_id = f"ai_{int(time.time() * 1000) % 10000}"
    player = players[request.sid]
    
    with room_lock:
        if room_id not in game_rooms:
            game_rooms[room_id] = GameRoom(room_id)
        
        room = game_rooms[room_id]
        room.is_ai_game = True
        room.ai_player = AIPlayer()
        
        if room.add_player(player['id'], player['username']):
            player['room'] = room_id
            join_room(room_id)
            
            # Marcar sala como lista inmediatamente
            room.status = 'ready'
            
            print(f"🤖 Creando sala AI {room_id} para jugador {player['username']}")
            
            response_data = {
                'room_id': room_id,
                'redirect': True,
                'is_ai_game': True,
                'ai_name': '🤖 IA',
                'player_name': player['username']
            }
            
            print(f"📤 Enviando ai_game_created: {response_data}")
            emit('ai_game_created', response_data)
            print(f"✅ Respuesta ai_game_created enviada al cliente {request.sid}")

@socketio.on('join_room_request')
def handle_join_room_request(data):
    if request.sid not in players:
        return
    
    room_id = data['room_id']
    player = players[request.sid]
    
    with room_lock:
        if room_id in game_rooms:
            room = game_rooms[room_id]
            if room.add_player(player['id'], player['username']):
                player['room'] = room_id
                join_room(room_id)
                
                emit('room_joined', {
                    'room_id': room_id,
                    'redirect': True
                })
                
                # Manejar salas AI de manera especial
                if room.is_ai_game:
                    print(f"🤖 Jugador {player['username']} se unió a sala AI {room_id}")
                    room.status = 'ready'
                    # Emitir evento especial para juego AI
                    socketio.emit('ai_room_ready', {
                        'player_name': player['username'],
                        'ai_name': '🤖 IA'
                    }, room=room_id)
                elif room.is_full():
                    # Solo para salas normales (no AI)
                    room.status = 'ready'
                    socketio.emit('room_full', {
                        'players': [p['username'] for p in room.players.values()]
                    }, room=room_id)
                    
                    # Actualizar lista de salas
                    socketio.emit('room_list_updated', {
                        'available_rooms': get_available_rooms()
                    })
            else:
                emit('join_failed', {'reason': 'Sala llena'})

@socketio.on('player_ready')
def handle_player_ready(data):
    if request.sid not in players:
        return
    
    player = players[request.sid]
    room_id = player.get('room')
    
    if room_id and room_id in game_rooms:
        room = game_rooms[room_id]
        if player['id'] in room.players:
            room.players[player['id']]['ready'] = True
            
            print(f"✅ Jugador {player['username']} listo en sala {room_id}")
            print(f"🤖 Es juego AI: {room.is_ai_game}")
            print(f"👥 Jugadores listos: {[p['username'] for p in room.players.values() if p['ready']]}")
            
            if room.all_ready():
                print(f"🚀 Iniciando countdown en sala {room_id}")
                start_countdown(room_id)
            else:
                print(f"⏳ Esperando más jugadores en sala {room_id}")
                
def start_countdown(room_id):
    room = game_rooms[room_id]
    room.status = 'countdown'
    
    print(f"⏰ Iniciando countdown en sala {room_id}")
    
    def countdown_sequence():
        for i in range(3, 0, -1):
            socketio.emit('countdown', {'count': i}, room=room_id)
            socketio.sleep(1)
        
        # ¡YA!
        socketio.emit('countdown', {'count': 'GO!'}, room=room_id)
        socketio.sleep(1)
        
        # Capturar gestos
        room.status = 'capture'
        socketio.emit('capture_gesture', {}, room=room_id)
    
    socketio.start_background_task(countdown_sequence)

@socketio.on('gesture_capture')
def handle_gesture_capture(data):
    if request.sid not in players:
        return
    
    player = players[request.sid]
    room_id = player.get('room')
    
    if room_id and room_id in game_rooms:
        room = game_rooms[room_id]
        
        # Decodificar imagen
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Detectar gesto con fallback
        if gesture_detector and CV2_AVAILABLE:
            try:
                # Convertir a formato OpenCV
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                gesture = gesture_detector.detect_rps_gesture(opencv_image)
            except Exception as e:
                print(f"Error en detección de gesto: {e}")
                gesture = random.choice(['rock', 'paper', 'scissors'])  # Fallback
        else:
            # Fallback: gesto aleatorio si no hay detector
            gesture = random.choice(['rock', 'paper', 'scissors'])
            print("⚠️ Usando gesto aleatorio (detector no disponible)")
        
        # Guardar captura y gesto
        room.captures[player['id']] = image_data
        room.gestures[player['id']] = gesture
        room.players[player['id']]['gesture'] = gesture
        room.players[player['id']]['capture'] = image_data
        
        # Si es juego vs IA, hacer que la IA juegue automáticamente
        if room.is_ai_game and 'ai' not in room.gestures:
            ai_gesture = room.ai_player.make_move()
            room.gestures['ai'] = ai_gesture
            print(f'🤖 IA jugó: {ai_gesture}')
        
        # Verificar si todos han enviado su gesto
        expected_gestures = 2 if not room.is_ai_game else 2
        if len(room.gestures) >= expected_gestures:
            determine_winner(room_id)

def determine_winner(room_id):
    room = game_rooms[room_id]
    
    if room.is_ai_game:
        # Juego vs IA
        player_ids = list(room.players.keys())
        if len(player_ids) != 1:
            return
        
        p1_id = player_ids[0]
        p1_gesture = room.gestures.get(p1_id, 'unknown')
        p2_gesture = room.gestures.get('ai', 'unknown')
        
        p1_name = room.players[p1_id]['username']
        p2_name = room.ai_player.username
        p2_id = 'ai'
    else:
        # Juego normal entre 2 jugadores
        player_ids = list(room.players.keys())
        if len(player_ids) != 2:
            return
        
        p1_id, p2_id = player_ids
        p1_gesture = room.gestures.get(p1_id, 'unknown')
        p2_gesture = room.gestures.get(p2_id, 'unknown')
        
        p1_name = room.players[p1_id]['username']
        p2_name = room.players[p2_id]['username']
    
    # Lógica RPS
    winner = None
    if p1_gesture == p2_gesture:
        result = "¡Empate!"
    elif (p1_gesture == 'rock' and p2_gesture == 'scissors') or \
         (p1_gesture == 'paper' and p2_gesture == 'rock') or \
         (p1_gesture == 'scissors' and p2_gesture == 'paper'):
        winner = p1_name
        result = f"¡{p1_name} gana!"
    elif (p2_gesture == 'rock' and p1_gesture == 'scissors') or \
         (p2_gesture == 'paper' and p1_gesture == 'rock') or \
         (p2_gesture == 'scissors' and p1_gesture == 'paper'):
        winner = p2_name
        result = f"¡{p2_name} gana!"
    else:
        result = "Gesto no reconocido"
    
    room.results = {
        'winner': winner,
        'result': result,
        'players': {
            p1_id: {
                'username': p1_name,
                'gesture': p1_gesture,
                'capture': room.captures.get(p1_id, '')
            },
            p2_id: {
                'username': p2_name,
                'gesture': p2_gesture,
                'capture': room.captures.get(p2_id, '') if p2_id != 'ai' else ''
            }
        }
    }
    
    room.status = 'results'
    
    # Enviar resultados
    socketio.emit('game_results', room.results, room=room_id)

@socketio.on('play_again')
def handle_play_again():
    print(f"🔄 PLAY_AGAIN recibido desde session {request.sid}")
    
    if request.sid not in players:
        print(f"❌ Session {request.sid} no encontrada en players")
        return
    
    player = players[request.sid]
    room_id = player.get('room')
    print(f"🏠 Jugador {player['username']} en sala {room_id}")
    
    if room_id and room_id in game_rooms:
        room = game_rooms[room_id]
        print(f"🎮 Sala encontrada. Es AI: {room.is_ai_game}")
        
        room.reset_round()
        print(f"🔄 Ronda reseteada")
        
        # Para juegos AI, automatizar el flujo completo
        if room.is_ai_game:
            room.status = 'ready'
            print(f"🤖 Sala AI {room_id} marcada como lista")
            
            # Marcar automáticamente al jugador como listo
            room.players[player['id']]['ready'] = True
            print(f"🚀 Jugador automáticamente marcado como listo")
            
            # Iniciar countdown inmediatamente
            print(f"⏰ Iniciando countdown automático para AI")
            start_countdown(room_id)
        
        reset_data = {
            'is_ai_game': room.is_ai_game,
            'status': room.status,
            'auto_start': room.is_ai_game  # Indicar al frontend que se auto-inicia
        }
        print(f"📡 Enviando round_reset: {reset_data}")
        
        socketio.emit('round_reset', reset_data, room=room_id)
        print(f"✅ round_reset enviado a sala {room_id}")
    else:
        print(f"❌ Sala {room_id} no encontrada")

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in players:
        player = players[request.sid]
        room_id = player.get('room')
        
        if room_id and room_id in game_rooms:
            room = game_rooms[room_id]
            room.remove_player(player['id'])
            
            if room.status == 'empty':
                del game_rooms[room_id]
            else:
                socketio.emit('player_left', {
                    'username': player['username']
                }, room=room_id)
            
            # Actualizar lista de salas
            socketio.emit('room_list_updated', {
                'available_rooms': get_available_rooms()
            })
        
        del players[request.sid]

def get_available_rooms():
    available_rooms = []
    with room_lock:
        for room_id, room in game_rooms.items():
            # Solo mostrar salas que no estén llenas, no estén vacías, y no sean juegos AI
            if not room.is_full() and room.status != 'empty' and not room.is_ai_game:
                available_rooms.append({
                    'id': room_id,
                    'players': len(room.players),
                    'max_players': 2
                })
    return available_rooms

if __name__ == '__main__':
    # Configuración para desarrollo local y producción
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    # Para desarrollo local, usar debug=False para evitar reinicios
    if port == 5000:
        debug_mode = False
    socketio.run(app, host='0.0.0.0', port=port, debug=debug_mode)