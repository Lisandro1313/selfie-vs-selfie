// Lobby.js - Version Ultra Simple
console.log('🎮 Iniciando RPS Lobby');

let socket = null;
let currentUser = null;
let isConnected = false;

// Inicialización cuando se carga la página
function initializeLobby() {
    console.log('🔧 Inicializando lobby');

    // Crear socket
    socket = io({
        autoConnect: true,
        reconnection: true,
        reconnectionAttempts: 5
    });

    setupSocketEvents();
    setupUIEvents();

    console.log('✅ Lobby inicializado');
}

// Configurar eventos del socket
function setupSocketEvents() {
    socket.on('connect', function () {
        console.log('✅ Socket conectado:', socket.id);
        isConnected = true;

        // Auto-reconectar si hay usuario guardado
        const savedUser = localStorage.getItem('rps_username');
        if (savedUser && !currentUser) {
            console.log('🔄 Auto-reconectando:', savedUser);
            joinLobby(savedUser);
        }
    });

    socket.on('disconnect', function () {
        console.log('❌ Socket desconectado');
        isConnected = false;
    });

    socket.on('lobby_joined', function (data) {
        console.log('🏠 Ingresado al lobby:', data);
        console.log('📊 Datos completos recibidos:', JSON.stringify(data, null, 2));
        currentUser = data.username;
        localStorage.setItem('rps_username', currentUser);

        // Debug: verificar elementos DOM
        const loginSection = document.getElementById('loginSection');
        const lobbySection = document.getElementById('lobbySection');
        console.log('🔍 LoginSection encontrada:', !!loginSection);
        console.log('🔍 LobbySection encontrada:', !!lobbySection);

        showLobby(data);
    });

    socket.on('room_created', function (data) {
        console.log('🏠 Sala creada:', data);
        if (data.redirect && data.room_id) {
            window.location.href = `/game/${data.room_id}`;
        }
    });

    socket.on('ai_game_created', function (data) {
        console.log('🤖 Juego IA creado:', data);
        if (data.redirect && data.room_id) {
            // Guardar información del juego AI en localStorage
            localStorage.setItem('ai_game_info', JSON.stringify({
                room_id: data.room_id,
                player_name: data.player_name,
                ai_name: data.ai_name,
                is_ai_game: true
            }));
            window.location.href = `/game/${data.room_id}`;
        }
    });
}

// Configurar eventos de la UI
function setupUIEvents() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.onsubmit = function (e) {
            e.preventDefault();
            const input = document.getElementById('username');
            if (input && input.value.trim()) {
                joinLobby(input.value.trim());
            }
        };
    }

    // Event delegation para botones
    document.onclick = function (e) {
        const id = e.target.id;
        console.log('🖱️ Click:', id);

        switch (id) {
            case 'createRoomBtn':
                createRoom();
                break;
            case 'playAiBtn':
                createAiGame();
                break;
            case 'logoutBtn':
                logout();
                break;
            case 'refreshBtn':
                refreshRooms();
                break;
        }
    };
}

// Funciones principales
function joinLobby(username) {
    if (!isConnected || !socket) {
        console.error('❌ Socket no conectado');
        return;
    }

    console.log('📤 Enviando join_lobby:', username);
    socket.emit('join_lobby', { username: username });
}

function createRoom() {
    if (!isConnected || !socket) {
        console.error('❌ Socket no conectado');
        return;
    }

    console.log('🏠 Creando sala normal');
    socket.emit('create_room');
}

function createAiGame() {
    if (!isConnected || !socket) {
        console.error('❌ Socket no conectado');
        return;
    }

    console.log('🤖 Creando juego vs IA');
    socket.emit('create_ai_game');
}

function logout() {
    console.log('🚪 Cerrando sesión');
    localStorage.removeItem('rps_username');
    currentUser = null;
    location.reload();
}

function refreshRooms() {
    console.log('🔄 Refrescando salas');
    if (socket && isConnected) {
        socket.emit('get_rooms');
    }
}

function showLobby(data) {
    console.log('🏠 Mostrando lobby para:', data.username);

    const loginSection = document.getElementById('loginSection');
    const lobbySection = document.getElementById('lobbySection');
    const playerName = document.getElementById('playerName');

    if (loginSection) {
        loginSection.classList.add('d-none');
        console.log('✅ Login section ocultada');
    }
    if (lobbySection) {
        lobbySection.classList.remove('d-none');
        console.log('✅ Lobby section mostrada');
    }
    if (playerName) {
        playerName.textContent = data.username;
        console.log('✅ Nombre actualizado:', data.username);
    }

    updateRooms(data.available_rooms || []);
}

function updateRooms(rooms) {
    console.log('📋 Actualizando salas:', rooms.length);

    const roomsList = document.getElementById('roomsList');
    const roomCount = document.getElementById('roomCount');

    if (roomCount) {
        roomCount.textContent = `${rooms.length} sala${rooms.length !== 1 ? 's' : ''}`;
    }

    if (!roomsList) return;

    if (rooms.length === 0) {
        roomsList.innerHTML = `
            <div class="col-12 text-center text-muted">
                <p>🏠 No hay salas disponibles</p>
                <p class="small">¡Sé el primero en crear una!</p>
            </div>
        `;
        return;
    }

    let html = '';
    rooms.forEach(room => {
        const isFull = room.players >= room.max_players;
        const statusClass = isFull ? 'bg-danger' : 'bg-success';
        const statusText = isFull ? 'Llena' : 'Disponible';

        html += `
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="card-title mb-0">🏠 ${room.id}</h6>
                            <span class="badge ${statusClass}">${statusText}</span>
                        </div>
                        <p class="card-text small text-muted">
                            👥 ${room.players}/${room.max_players} jugadores
                        </p>
                        ${!isFull ? `
                            <button class="btn btn-primary btn-sm w-100" onclick="joinRoom('${room.id}')">
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

    roomsList.innerHTML = html;
}

function joinRoom(roomId) {
    console.log('🚪 Uniéndose a sala:', roomId);
    if (socket && isConnected) {
        socket.emit('join_room_request', { room_id: roomId });
    }
}

// Inicializar cuando se carga el DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeLobby);
} else {
    initializeLobby();
}

console.log('✅ Script lobby cargado completamente');