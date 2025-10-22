from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_secret'

# Inicialización simple de SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('🔗 Cliente conectado')
    emit('connected', {'status': 'success'})

@socketio.on('disconnect')
def handle_disconnect():
    print('🔌 Cliente desconectado')

@socketio.on('join_lobby')
def handle_join_lobby(data):
    print('🏠 Join lobby:', data)
    username = data.get('username', 'Usuario')
    
    emit('lobby_joined', {
        'status': 'success',
        'username': username,
        'available_rooms': []
    })

@socketio.on('create_room')
def handle_create_room():
    print('🏠 Crear sala solicitada')
    room_id = f"room_{int(time.time())}"
    
    emit('room_created', {
        'status': 'success',
        'room_id': room_id,
        'redirect': True
    })

if __name__ == '__main__':
    import time
    print('🚀 Iniciando servidor de prueba...')
    try:
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f'❌ Error: {e}')
        sys.exit(1)