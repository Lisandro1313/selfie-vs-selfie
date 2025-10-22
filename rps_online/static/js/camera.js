// Camera JavaScript - Manejo de cámara web
class CameraManager {
    constructor() {
        this.stream = null;
        this.video = null;
        this.canvas = null;
        this.context = null;
        this.isCapturing = false;

        this.init();
    }

    init() {
        this.video = document.getElementById('videoElement');
        this.canvas = document.getElementById('captureCanvas');
        this.context = this.canvas.getContext('2d');
    }

    async startCamera() {
        try {
            // Solicitar acceso a la cámara
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                },
                audio: false
            });

            // Conectar stream al elemento video
            this.video.srcObject = this.stream;

            return new Promise((resolve) => {
                this.video.onloadedmetadata = () => {
                    resolve(true);
                };
            });

        } catch (error) {
            console.error('Error accediendo a la cámara:', error);
            throw new Error('No se pudo acceder a la cámara. Asegúrate de dar permisos.');
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => {
                track.stop();
            });
            this.stream = null;
        }

        if (this.video) {
            this.video.srcObject = null;
        }
    }

    captureImage() {
        if (!this.video || !this.canvas || !this.context) {
            throw new Error('Cámara no inicializada');
        }

        // Dibujar el frame actual del video en el canvas
        this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);

        // Convertir a base64
        const imageData = this.canvas.toDataURL('image/jpeg', 0.8);

        return imageData;
    }

    isActive() {
        return this.stream && this.stream.active;
    }

    // Verificar si el navegador soporta getUserMedia
    static isSupported() {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
    }

    // Verificar permisos de cámara
    async checkPermissions() {
        try {
            const result = await navigator.permissions.query({ name: 'camera' });
            return result.state; // 'granted', 'denied', o 'prompt'
        } catch (error) {
            // Si no se puede verificar, intentamos acceso directo
            return 'unknown';
        }
    }
}

// Hacer disponible globalmente
window.CameraManager = CameraManager;