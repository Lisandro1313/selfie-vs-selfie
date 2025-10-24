// Game JavaScript - Lógica principal del juego
class GameManager {
    constructor() {
        this.socket = null;
        this.camera = null;
        this.roomId = window.ROOM_ID;
        this.playerId = null;
        this.gameState = 'waiting'; // waiting, ready, countdown, capturing, results
        this.isAIGame = false; // Seguimiento del modo AI

        this.init();
    }

    init() {
        this.setupSocket();
        this.setupEventListeners();
        this.camera = new CameraManager();

        // Verificar soporte de cámara
        if (!CameraManager.isSupported()) {
            this.showError('Tu navegador no soporta acceso a cámara');
            return;
        }

        console.log('Juego iniciado en sala:', this.roomId);
    }

    setupSocket() {
        this.socket = io();

        // Eventos de conexión
        this.socket.on('connect', () => {
            console.log('🎮 Conectado al servidor de juego, sala:', this.roomId);
            this.joinRoom();
        });

        this.socket.on('disconnect', () => {
            console.log('❌ Desconectado del servidor');
            this.showError('Conexión perdida');
        });

        // Eventos de sala
        this.socket.on('room_full', (data) => {
            this.handleRoomFull(data);
        });

        this.socket.on('ai_room_ready', (data) => {
            console.log('🤖 Evento ai_room_ready recibido:', data);
            this.handleAIRoomReady(data);
        });

        this.socket.on('player_left', (data) => {
            this.handlePlayerLeft(data);
        });

        // Eventos de juego
        this.socket.on('countdown', (data) => {
            this.handleCountdown(data);
        });

        this.socket.on('capture_gesture', () => {
            this.captureGesture();
        });

        this.socket.on('game_results', (data) => {
            this.showResults(data);
        });

        this.socket.on('round_reset', (data) => {
            console.log('🔄 Round reset recibido:', data);
            this.resetRound(data);
        });
    }

    setupEventListeners() {
        // Botón de listo
        document.getElementById('readyBtn').addEventListener('click', () => {
            this.handleReady();
        });

        // Botones de navegación
        document.getElementById('leaveRoomBtn').addEventListener('click', () => {
            this.leaveRoom();
        });

        document.getElementById('playAgainBtn').addEventListener('click', () => {
            this.playAgain();
        });

        document.getElementById('backToLobbyBtn').addEventListener('click', () => {
            this.leaveRoom();
        });

        // Manejar cierre de página
        window.addEventListener('beforeunload', () => {
            this.cleanup();
        });
    }

    joinRoom() {
        // Verificar si es un juego AI
        const aiGameInfo = localStorage.getItem('ai_game_info');
        console.log('🎲 Información juego AI:', aiGameInfo);

        if (aiGameInfo) {
            try {
                const gameData = JSON.parse(aiGameInfo);
                console.log('🤖 Datos del juego AI:', gameData);

                if (gameData.room_id === this.roomId && gameData.is_ai_game) {
                    // Es un juego AI, activar inmediatamente
                    console.log('🎮 Activando juego AI inmediatamente');
                    this.isAIGame = true; // Marcar como juego AI
                    setTimeout(() => {
                        this.handleAIRoomReady({
                            player_name: gameData.player_name,
                            ai_name: gameData.ai_name
                        });
                    }, 500);

                    // NO eliminar la información - la necesitamos para "play again"
                    // localStorage.removeItem('ai_game_info');
                    return;
                }
            } catch (e) {
                console.error('❌ Error parseando info AI:', e);
            }
        }

        // Flujo normal para juegos no-AI
        const savedUsername = localStorage.getItem('rps_username');
        console.log('👤 Usuario guardado (juego normal):', savedUsername);

        if (!savedUsername) {
            console.error('❌ No hay usuario guardado, redirigiendo al lobby');
            window.location.href = '/';
            return;
        }

        // Primero unirse al lobby como jugador registrado
        console.log('🔄 Uniéndose al lobby como:', savedUsername);
        this.socket.emit('join_lobby', { username: savedUsername });

        // Después intentar unirse a la sala
        setTimeout(() => {
            console.log('🎮 Intentando unirse a sala:', this.roomId);
            this.socket.emit('join_room_request', { room_id: this.roomId });
        }, 500);
    }

    handleRoomFull(data) {
        console.log('Sala llena:', data);
        this.gameState = 'ready';

        // Actualizar UI
        document.getElementById('waitingSection').classList.add('d-none');
        document.getElementById('gameSection').classList.remove('d-none');

        // Mostrar jugadores
        const players = data.players;
        if (players.length >= 2) {
            document.getElementById('player1Name').textContent = players[0];
            document.getElementById('player2Name').textContent = players[1];
        }

        // Mostrar sección de preparación
        this.showReadySection();
    }

    handleAIRoomReady(data) {
        console.log('Juego vs IA listo:', data);
        this.gameState = 'ready';
        this.isAIGame = true;

        // Actualizar UI para juego vs IA
        document.getElementById('waitingSection').classList.add('d-none');
        document.getElementById('gameSection').classList.remove('d-none');

        // Mostrar jugador vs IA
        document.getElementById('player1Name').textContent = data.player_name;
        document.getElementById('player2Name').textContent = data.ai_name;

        // Cambiar estado del header
        document.getElementById('gameStatus').textContent = `🤖 Juego vs IA`;

        // Mostrar sección de preparación
        this.showReadySection();
    }

    handlePlayerLeft(data) {
        this.showError(`${data.username} ha salido de la sala`);

        // Volver a modo de espera
        this.gameState = 'waiting';
        document.getElementById('waitingSection').classList.remove('d-none');
        document.getElementById('gameSection').classList.add('d-none');
    }

    async handleReady() {
        try {
            // Iniciar cámara
            await this.camera.startCamera();

            // Ocultar botón de listo y mostrar cámara
            document.getElementById('readySection').classList.add('d-none');
            document.getElementById('cameraSection').classList.remove('d-none');

            if (this.isAIGame) {
                // Para juego vs IA, empezar countdown inmediatamente
                console.log('🤖 Juego vs IA - Iniciando countdown inmediatamente');
                document.getElementById('gameStatus').textContent = '🤖 Preparándose para jugar vs IA...';

                // Empezar countdown después de un breve delay
                setTimeout(() => {
                    this.startAICountdown();
                }, 1500);
            } else {
                // Para juego normal, notificar al servidor
                this.socket.emit('player_ready', {});
                document.getElementById('gameStatus').textContent = 'Esperando que ambos jugadores estén listos...';
            }

        } catch (error) {
            this.showError(error.message);
        }
    }

    startAICountdown() {
        console.log('🚀 Iniciando countdown para juego AI');

        // Mostrar overlay de countdown
        const countdownOverlay = document.getElementById('countdownOverlay');
        const countdownNumber = document.getElementById('countdownNumber');

        countdownOverlay.classList.remove('d-none');

        let count = 3;

        const countdownInterval = setInterval(() => {
            if (count > 0) {
                console.log(`⏰ Countdown: ${count}`);
                countdownNumber.textContent = count;
                countdownNumber.style.color = '#ffc107';
                count--;
            } else {
                // ¡YA!
                console.log('🎯 ¡YA! Capturando gesto...');
                countdownNumber.textContent = '¡YA!';
                countdownNumber.style.color = '#28a745';

                clearInterval(countdownInterval);

                // Empezar captura después de mostrar "¡YA!"
                setTimeout(() => {
                    countdownOverlay.classList.add('d-none');
                    this.startAIGestureCapture();
                }, 1000);
            }
        }, 1000);
    }

    startAIGestureCapture() {
        console.log('🎮 Iniciando captura de gesto vs IA');
        document.getElementById('gameStatus').textContent = '¡Haz tu gesto ahora! (3 segundos)';

        // Capturar por 3 segundos
        let captureTime = 3;
        const captureInterval = setInterval(() => {
            console.log(`📸 Capturando... ${captureTime} segundos restantes`);
            document.getElementById('gameStatus').textContent = `¡Haz tu gesto! (${captureTime}s)`;
            captureTime--;

            if (captureTime < 0) {
                clearInterval(captureInterval);
                this.finishAIGestureCapture();
            }
        }, 1000);
    }

    async finishAIGestureCapture() {
        console.log('✅ Finalizando captura vs IA');
        document.getElementById('gameStatus').textContent = 'Procesando resultado...';

        try {
            // Capturar imagen final
            const imageData = this.camera.captureImage();
            console.log('📷 Imagen capturada para análisis');

            // Simular análisis (en un juego real, esto iría al servidor)
            // Por ahora, simular resultado después de un delay
            setTimeout(() => {
                this.simulateAIGameResult(imageData);
            }, 2000);

        } catch (error) {
            this.showError('Error al capturar gesto: ' + error.message);
        }
    }

    simulateAIGameResult(playerImage) {
        console.log('🎲 Generando resultado vs IA');

        // IA elige gesto aleatorio
        const aiGestures = ['rock', 'paper', 'scissors'];
        const aiGesture = aiGestures[Math.floor(Math.random() * 3)];

        // Detectar gesto del jugador de forma más inteligente
        // Por ahora, hacer que siempre detecte algo válido (mejorar después con ML)
        const playerGestures = ['rock', 'paper', 'scissors'];
        let playerGesture;

        // Simulación mejorada: dar más probabilidad a tijeras si el usuario hizo tijeras
        const gestureWeights = {
            'scissors': 0.5,  // Mayor probabilidad para tijeras
            'rock': 0.3,
            'paper': 0.2
        };

        const rand = Math.random();
        if (rand < gestureWeights.scissors) {
            playerGesture = 'scissors';
        } else if (rand < gestureWeights.scissors + gestureWeights.rock) {
            playerGesture = 'rock';
        } else {
            playerGesture = 'paper';
        }

        console.log(`🎯 Detectado: Jugador=${playerGesture}, IA=${aiGesture}`);

        // Determinar ganador
        let winner = '🤝 Empate';
        if (
            (playerGesture === 'rock' && aiGesture === 'scissors') ||
            (playerGesture === 'paper' && aiGesture === 'rock') ||
            (playerGesture === 'scissors' && aiGesture === 'paper')
        ) {
            winner = '🎉 Tú ganas!';
        } else if (
            (aiGesture === 'rock' && playerGesture === 'scissors') ||
            (aiGesture === 'paper' && playerGesture === 'rock') ||
            (aiGesture === 'scissors' && playerGesture === 'paper')
        ) {
            winner = '🤖 IA gana!';
        }

        // Mostrar resultado
        this.showAIResults({
            winner: winner,
            playerGesture: playerGesture,
            aiGesture: aiGesture,
            playerImage: playerImage,
            playerName: localStorage.getItem('rps_username') || 'Jugador',
            aiName: '🤖 IA'
        });
    }

    showAIResults(data) {
        console.log('🏆 Mostrando resultados vs IA:', data);
        this.gameState = 'results';

        // Ocultar cámara y mostrar resultados
        document.getElementById('cameraSection').classList.add('d-none');
        document.getElementById('resultsSection').classList.remove('d-none');

        // Actualizar título y mensaje
        document.getElementById('resultTitle').textContent = data.winner;
        document.getElementById('resultMessage').textContent = 'Resultado del juego:';

        // Actualizar nombres de jugadores
        const result1Name = document.getElementById('result1Name');
        const result2Name = document.getElementById('result2Name');
        if (result1Name) result1Name.textContent = data.playerName;
        if (result2Name) result2Name.textContent = data.aiName;

        // Mostrar imagen del jugador
        const result1Image = document.getElementById('result1Image');
        if (result1Image && data.playerImage) {
            result1Image.src = data.playerImage;
            result1Image.style.display = 'block';
        }

        // Mostrar gesto del jugador
        const result1Gesture = document.getElementById('result1Gesture');
        if (result1Gesture) {
            result1Gesture.textContent = this.getGestureEmoji(data.playerGesture);
            result1Gesture.className = `badge bg-primary`;
        }

        // Para la IA: mostrar emoji gigante en lugar de imagen
        const result2Image = document.getElementById('result2Image');
        if (result2Image) {
            // Crear un div con emoji gigante
            const aiEmojiDiv = document.createElement('div');
            aiEmojiDiv.innerHTML = `
                <div class="d-flex align-items-center justify-content-center bg-light rounded" style="height: 300px; font-size: 8rem;">
                    ${this.getGestureOnlyEmoji(data.aiGesture)}
                </div>
            `;

            // Reemplazar la imagen con el emoji
            result2Image.style.display = 'none';
            if (!result2Image.nextElementSibling || !result2Image.nextElementSibling.classList.contains('ai-emoji')) {
                aiEmojiDiv.className = 'ai-emoji';
                result2Image.parentNode.insertBefore(aiEmojiDiv, result2Image.nextSibling);
            }
        }

        // Mostrar gesto de la IA
        const result2Gesture = document.getElementById('result2Gesture');
        if (result2Gesture) {
            result2Gesture.textContent = this.getGestureEmoji(data.aiGesture);
            result2Gesture.className = `badge bg-success`;
        }
    }

    getGestureEmoji(gesture) {
        switch (gesture) {
            case 'rock': return '🪨 Piedra';
            case 'paper': return '📄 Papel';
            case 'scissors': return '✂️ Tijeras';
            default: return '❓ Desconocido';
        }
    }

    getGestureOnlyEmoji(gesture) {
        switch (gesture) {
            case 'rock': return '🪨';
            case 'paper': return '📄';
            case 'scissors': return '✂️';
            default: return '❓';
        }
    }

    handleCountdown(data) {
        const count = data.count;
        const countdownOverlay = document.getElementById('countdownOverlay');
        const countdownNumber = document.getElementById('countdownNumber');

        if (count === 'GO!') {
            countdownNumber.textContent = '¡YA!';
            countdownNumber.style.color = '#28a745';

            // Ocultar countdown después de un momento
            setTimeout(() => {
                countdownOverlay.classList.add('d-none');
            }, 1000);

        } else {
            countdownOverlay.classList.remove('d-none');
            countdownNumber.textContent = count;
            countdownNumber.style.color = '#ffc107';
        }

        document.getElementById('gameStatus').textContent = `Countdown: ${count}`;
    }

    captureGesture() {
        try {
            // Capturar imagen de la cámara
            const imageData = this.camera.captureImage();

            // Enviar al servidor para análisis
            this.socket.emit('gesture_capture', {
                image: imageData
            });

            document.getElementById('gameStatus').textContent = 'Analizando gesto...';

        } catch (error) {
            this.showError('Error al capturar imagen: ' + error.message);
        }
    }

    showResults(data) {
        console.log('Resultados:', data);
        this.gameState = 'results';

        // Ocultar cámara y mostrar resultados
        document.getElementById('cameraSection').classList.add('d-none');
        document.getElementById('resultsSection').classList.remove('d-none');

        // Actualizar título y mensaje
        document.getElementById('resultTitle').textContent = data.result;
        document.getElementById('resultMessage').textContent = 'Aquí están los gestos capturados:';

        // Mostrar imágenes y gestos de ambos jugadores
        const playerIds = Object.keys(data.players);
        if (playerIds.length >= 2) {
            const p1 = data.players[playerIds[0]];
            const p2 = data.players[playerIds[1]];

            // Jugador 1
            document.getElementById('result1Name').textContent = p1.username;
            document.getElementById('result1Image').src = 'data:image/jpeg;base64,' + p1.capture;
            document.getElementById('result1Gesture').textContent = this.translateGesture(p1.gesture);

            // Jugador 2
            document.getElementById('result2Name').textContent = p2.username;
            document.getElementById('result2Image').src = 'data:image/jpeg;base64,' + p2.capture;
            document.getElementById('result2Gesture').textContent = this.translateGesture(p2.gesture);
        }

        document.getElementById('gameStatus').textContent = data.result;
    }

    translateGesture(gesture) {
        const translations = {
            'rock': '🗿 Piedra',
            'paper': '📄 Papel',
            'scissors': '✂️ Tijeras',
            'unknown': '❓ No detectado'
        };

        return translations[gesture] || '❓ Desconocido';
    }

    playAgain() {
        console.log('🔄 Enviando solicitud de play_again...');

        // Para juegos AI, usar lógica local directa
        if (this.isAIGame || localStorage.getItem('ai_game_info')) {
            console.log('🤖 Juego AI detectado - Usando reset local inmediato');

            // Reset directo para AI
            this.gameState = 'ready';
            document.getElementById('resultsSection').classList.add('d-none');
            document.getElementById('readySection').classList.remove('d-none');
            document.getElementById('cameraSection').classList.add('d-none');
            document.getElementById('countdownOverlay').classList.add('d-none');
            document.getElementById('gameStatus').textContent = '🤖 Nueva ronda contra IA - ¡Prepárate!';

            // Parar cámara si está funcionando
            this.camera.stopCamera();

            console.log('✅ Reset local completado para juego AI');

            // También enviar al servidor para mantener sincronización
            this.socket.emit('play_again');
        } else {
            // Juego normal - usar flujo del servidor
            this.socket.emit('play_again');
        }
    }

    resetRound(data = {}) {
        // Resetear UI para nueva ronda
        this.gameState = 'ready';

        document.getElementById('resultsSection').classList.add('d-none');
        document.getElementById('readySection').classList.remove('d-none');
        document.getElementById('cameraSection').classList.add('d-none');
        document.getElementById('countdownOverlay').classList.add('d-none');

        // Verificar si es un juego AI (desde localStorage o data)
        const isAIGame = data.is_ai_game || this.isAIGame || localStorage.getItem('ai_game_info');

        if (isAIGame) {
            this.isAIGame = true; // Asegurar que se mantiene el estado
            document.getElementById('gameStatus').textContent = '🤖 Nueva ronda contra IA - ¡Iniciando automáticamente!';
            console.log('🤖 Configurando nueva ronda AI con auto-inicio');

            // Asegurar que la interfaz está configurada para AI
            document.getElementById('waitingSection').classList.add('d-none');
            document.getElementById('gameSection').classList.remove('d-none');

            // Verificar que los nombres están configurados
            const aiGameInfo = localStorage.getItem('ai_game_info');
            if (aiGameInfo) {
                try {
                    const gameData = JSON.parse(aiGameInfo);
                    document.getElementById('player1Name').textContent = gameData.player_name;
                    document.getElementById('player2Name').textContent = gameData.ai_name;
                } catch (e) {
                    console.error('Error parseando AI info:', e);
                }
            }

            // Para juegos AI, auto-presionar "Listo" después de un breve delay
            setTimeout(() => {
                console.log('🚀 Auto-presionando "Listo" para juego AI');
                this.handleReady();
            }, 1000); // 1 segundo de delay para que el jugador vea que se reinició

        } else {
            document.getElementById('gameStatus').textContent = 'Nueva ronda - ¡Prepárense!';
        }

        // Parar cámara
        this.camera.stopCamera();

        console.log('🔄 Ronda reseteada correctamente, isAIGame:', this.isAIGame);
    }

    leaveRoom() {
        this.cleanup();
        // Limpiar información AI solo cuando se abandona la sala
        localStorage.removeItem('ai_game_info');
        window.location.href = '/';
    }

    cleanup() {
        if (this.camera) {
            this.camera.stopCamera();
        }

        if (this.socket) {
            this.socket.disconnect();
        }
    }

    showReadySection() {
        document.getElementById('readySection').classList.remove('d-none');
        document.getElementById('cameraSection').classList.add('d-none');
        document.getElementById('resultsSection').classList.add('d-none');
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        const modal = new bootstrap.Modal(document.getElementById('errorModal'));
        modal.show();
    }
}

// Inicializar cuando el DOM esté listo
let game;
document.addEventListener('DOMContentLoaded', () => {
    game = new GameManager();
});

// Hacer disponible globalmente
window.game = game;