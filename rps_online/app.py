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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rps_online_secret_2025'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

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

@app.route('/game/<room_id>')
def game(room_id):
    return render_template('game.html', room_id=room_id)

@socketio.on('join_lobby')
def handle_join_lobby(data):
    print(f"Usuario intentando unirse al lobby: {data}")
    username = data['username']
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
    if request.sid not in players:
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
    if request.sid not in players:
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
            
            emit('ai_game_created', {
                'room_id': room_id,
                'redirect': True,
                'is_ai_game': True,
                'ai_name': '🤖 IA',
                'player_name': player['username']
            })

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
            
            if room.all_ready():
                start_countdown(room_id)

def start_countdown(room_id):
    room = game_rooms[room_id]
    room.status = 'countdown'
    
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
    if request.sid not in players:
        return
    
    player = players[request.sid]
    room_id = player.get('room')
    
    if room_id and room_id in game_rooms:
        room = game_rooms[room_id]
        room.reset_round()
        
        socketio.emit('round_reset', {}, room=room_id)

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
            if not room.is_full() and room.status != 'empty':
                available_rooms.append({
                    'id': room_id,
                    'players': len(room.players),
                    'max_players': 2
                })
    return available_rooms

if __name__ == '__main__':
    # Configuración para producción
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
    socketio.run(app, host='0.0.0.0', port=port, debug=debug_mode)