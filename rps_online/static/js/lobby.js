// Lobby JavaScript - Manejo del lobby principal
class LobbyManager {
    constructor() {
        this.socket = null;
        this.username = '';
        this.playerId = '';
        this.currentRooms = [];

        this.init();
    }

    init() {
        this.setupSocket();
        this.setupEventListeners();
        this.showLoginSection();
    }

    setupSocket() {
        this.socket = io();

        // Eventos del socket
        this.socket.on('connect', () => {
            console.log('✅ Conectado al servidor');
        });

        this.socket.on('disconnect', () => {
            console.log('❌ Desconectado del servidor');
            this.showError('Conexión perdida. Intentando reconectar...');
        });

        this.socket.on('lobby_joined', (data) => {
            console.log('✅ Lobby joined:', data);
            this.playerId = data.player_id;
            this.username = data.username;
            this.currentRooms = data.available_rooms;

            this.showLobbySection();
            this.updateRoomsList();
        });

        this.socket.on('room_created', (data) => {
            if (data.redirect) {
                window.location.href = `/game/${data.room_id}`;
            }
        });

        this.socket.on('room_joined', (data) => {
            if (data.redirect) {
                window.location.href = `/game/${data.room_id}`;
            }
        });

        this.socket.on('join_failed', (data) => {
            this.showError(data.reason);
        });

        this.socket.on('room_list_updated', (data) => {
            this.currentRooms = data.available_rooms;
            this.updateRoomsList();
        });
    }

    setupEventListeners() {
        // Login form
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // Create room button
        document.getElementById('createRoomBtn').addEventListener('click', () => {
            this.createRoom();
        });

        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshRooms();
        });
    }

    handleLogin() {
        const usernameInput = document.getElementById('username');
        const username = usernameInput.value.trim();

        if (username.length < 2) {
            this.showError('El nombre debe tener al menos 2 caracteres');
            return;
        }

        if (username.length > 20) {
            this.showError('El nombre no puede tener más de 20 caracteres');
            return;
        }

        console.log('🚀 Enviando join_lobby con username:', username);
        this.showLoading();
        this.socket.emit('join_lobby', { username: username });
    }

    createRoom() {
        this.socket.emit('create_room');
    }

    joinRoom(roomId) {
        this.socket.emit('join_room_request', { room_id: roomId });
    }

    refreshRooms() {
        // El servidor automáticamente envía actualizaciones,
        // pero podemos solicitar una actualización manual
        location.reload();
    }

    showLoginSection() {
        document.getElementById('loginSection').classList.remove('d-none');
        document.getElementById('lobbySection').classList.add('d-none');
        document.getElementById('username').focus();
    }

    showLobbySection() {
        document.getElementById('loginSection').classList.add('d-none');
        document.getElementById('lobbySection').classList.remove('d-none');
        document.getElementById('playerName').textContent = this.username;
        this.hideLoading();
    }

    updateRoomsList() {
        const roomsList = document.getElementById('roomsList');
        const roomCount = document.getElementById('roomCount');

        if (this.currentRooms.length === 0) {
            roomsList.innerHTML = `
                <div class="col-12 text-center text-muted">
                    <p>🏠 No hay salas disponibles</p>
                    <p class="small">¡Sé el primero en crear una!</p>
                </div>
            `;
            roomCount.textContent = '0 salas';
            return;
        }

        roomCount.textContent = `${this.currentRooms.length} sala${this.currentRooms.length !== 1 ? 's' : ''}`;

        let roomsHTML = '';
        this.currentRooms.forEach(room => {
            const isFull = room.players >= room.max_players;
            const statusClass = isFull ? 'bg-danger' : 'bg-success';
            const statusText = isFull ? 'Llena' : 'Disponible';

            roomsHTML += `
                <div class="col-md-6 col-lg-4 mb-3">
                    <div class="card room-card ${isFull ? 'full' : ''}" 
                         onclick="${isFull ? '' : `lobby.joinRoom('${room.id}')`}">
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

    showLoading() {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        modal.show();
    }

    hideLoading() {
        const modalElement = document.getElementById('loadingModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) {
            modal.hide();
        }
    }

    showError(message) {
        this.hideLoading();

        // Crear toast de error
        const toastHTML = `
            <div class="toast align-items-center text-white bg-danger border-0 position-fixed top-0 end-0 m-3" 
                 role="alert" style="z-index: 9999;">
                <div class="d-flex">
                    <div class="toast-body">
                        ⚠️ ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                            data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', toastHTML);

        const toastElement = document.querySelector('.toast:last-child');
        const toast = new bootstrap.Toast(toastElement);
        toast.show();

        // Remover el toast después de que se oculte
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }
}

// Inicializar cuando el DOM esté listo
let lobby;
document.addEventListener('DOMContentLoaded', () => {
    lobby = new LobbyManager();
});

// Hacer disponible globalmente para los onclick
window.lobby = lobby;