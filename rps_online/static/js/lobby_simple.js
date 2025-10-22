// Versión simplificada para debug
console.log('🎮 Lobby.js cargado');

let socket;
let username = '';

document.addEventListener('DOMContentLoaded', function () {
    console.log('📋 DOM cargado');

    // Inicializar socket
    socket = io();

    socket.on('connect', function () {
        console.log('✅ Socket conectado');

        // Si ya hay un username guardado, reconectar automáticamente
        const savedUsername = localStorage.getItem('rps_username');
        if (savedUsername) {
            console.log('🔄 Reconectando como:', savedUsername);
            username = savedUsername;
            socket.emit('join_lobby', { username: username });
        }
    });

    socket.on('disconnect', function () {
        console.log('❌ Socket desconectado');
    });

    socket.on('lobby_joined', function (data) {
        console.log('✅ Lobby joined:', data);
        // Guardar username para futuras reconexiones
        localStorage.setItem('rps_username', data.username);
        showLobby(data);
    });

    // Manejar formulario de login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            console.log('📝 Formulario enviado');

            const usernameInput = document.getElementById('username');
            username = usernameInput.value.trim();

            console.log('🚀 Username:', username);

            if (username.length < 2) {
                alert('El nombre debe tener al menos 2 caracteres');
                return;
            }

            console.log('📤 Enviando join_lobby');
            localStorage.setItem('rps_username', username);
            socket.emit('join_lobby', { username: username });
        });
    }

    // Botones de sala y IA - Event delegation global
    document.addEventListener('click', function (e) {
        console.log('🖱️ Click detectado en:', e.target.id);

        if (e.target.id === 'createRoomBtn') {
            console.log('🏠 Creando sala');
            if (socket && socket.connected) {
                socket.emit('create_room');
            } else {
                console.error('❌ Socket no conectado');
            }
        } else if (e.target.id === 'playAiBtn') {
            console.log('🤖 Creando juego vs IA');
            if (socket && socket.connected) {
                socket.emit('create_ai_game');
            } else {
                console.error('❌ Socket no conectado');
            }
        } else if (e.target.id === 'logoutBtn') {
            console.log('🚪 Cerrando sesión');
            localStorage.removeItem('rps_username');
            location.reload();
        }
    });

    // Manejar eventos de sala
    socket.on('room_created', function (data) {
        console.log('🏠 Sala creada:', data);
        if (data.redirect) {
            window.location.href = `/game/${data.room_id}`;
        }
    });

    socket.on('room_joined', function (data) {
        console.log('🚪 Sala unida:', data);
        if (data.redirect) {
            window.location.href = `/game/${data.room_id}`;
        }
    });

    socket.on('ai_game_created', function (data) {
        console.log('🤖 Juego vs IA creado:', data);
        if (data.redirect) {
            window.location.href = `/game/${data.room_id}`;
        }
    });

});

function showLobby(data) {
    console.log('🏠 Mostrando lobby');

    // Ocultar login, mostrar lobby
    const loginSection = document.getElementById('loginSection');
    const lobbySection = document.getElementById('lobbySection');

    if (loginSection) loginSection.classList.add('d-none');
    if (lobbySection) lobbySection.classList.remove('d-none');

    // Actualizar nombre
    const playerName = document.getElementById('playerName');
    if (playerName) playerName.textContent = data.username;

    // Actualizar salas
    updateRooms(data.available_rooms);
}

function updateRooms(rooms) {
    console.log('📋 Actualizando salas:', rooms);

    const roomsList = document.getElementById('roomsList');
    const roomCount = document.getElementById('roomCount');

    if (!roomsList || !roomCount) return;

    if (rooms.length === 0) {
        roomsList.innerHTML = `
            <div class="col-12 text-center text-muted">
                <p>🏠 No hay salas disponibles</p>
                <p class="small">¡Sé el primero en crear una!</p>
            </div>
        `;
        roomCount.textContent = '0 salas';
        return;
    }

    roomCount.textContent = `${rooms.length} sala${rooms.length !== 1 ? 's' : ''}`;

    let roomsHTML = '';
    rooms.forEach(room => {
        const isFull = room.players >= room.max_players;
        const statusClass = isFull ? 'bg-danger' : 'bg-success';
        const statusText = isFull ? 'Llena' : 'Disponible';

        roomsHTML += `
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card room-card ${isFull ? 'full' : ''}" 
                     ${isFull ? '' : `onclick="joinRoom('${room.id}')"`}>
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="card-title mb-0">🏠 ${room.id}</h6>
                            <span class="badge ${statusClass}">${statusText}</span>
                        </div>
                        <p class="card-text small text-muted">
                            👥 ${room.players}/${room.max_players} jugadores
                        </p>
                        ${!isFull ? `
                            <button class="btn btn-primary btn-sm w-100">
                                Unirse 🚀
                            </button>
                        ` : `
                            <button class="btn btn-secondary btn-sm w-100" disabled>
                                Sala Llena ⚠️
                            </button>
                        `}
                    </div>
                </div>
            </div>
        `;
    });

    roomsList.innerHTML = roomsHTML;
}

function joinRoom(roomId) {
    console.log('🚪 Uniéndose a sala:', roomId);
    socket.emit('join_room_request', { room_id: roomId });
}

console.log('✅ Lobby.js inicializado');